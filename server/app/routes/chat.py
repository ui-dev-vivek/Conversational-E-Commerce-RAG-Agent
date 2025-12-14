from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from datetime import datetime
import logging
import re

from ..config.llm_config import LLM
from ..validators.chat_validator import (
    ChatMessageInput, ChatMessageOutput, 
    ProductData, CartSummary, CartItemData, OrderData
)
from ..services.rag.retrieval import Retrieval
from ..agents.tools.tool_registry import tool_registry
from ..services.llm_intent_detector import detect_intent_with_llm, extract_tool_parameters

logger = logging.getLogger(__name__)

router = APIRouter()
llm = LLM.invoke()
retrieval = Retrieval(k=3)

# Simple per-user in-memory store
user_histories = {}


def extract_keywords(query: str) -> str:
    """
    Extract product search keywords from natural language query.
    
    Examples:
        "Show me candles" -> "candles"
        "I want to buy kurti" -> "kurti"
        "Find lavender products" -> "lavender"
    """
    # Remove common phrases
    stop_words = [
        'show', 'me', 'find', 'search', 'looking', 'for', 'want', 'to', 'buy',
        'get', 'need', 'i', 'am', 'some', 'any', 'the', 'a', 'an',
        'products', 'items', 'things', 'stuff',
        'dikhao', 'chahiye', 'dhundo', 'kharidna', 'hai'
    ]
    
    # Convert to lowercase and split
    words = query.lower().split()
    
    # Filter out stop words
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Join remaining words
    result = ' '.join(keywords)
    
    # If no keywords found, return original query
    return result if result else query


def format_context(docs):
    """Format retrieved documents into context string"""
    if not docs:
        return "No relevant information found."
    return "\n".join([f"- {doc.page_content}" for doc in docs])


def create_rag_chain():
    """
    Create RAG chain: Retrieve → Format → Prompt → LLM
    
    Flow:
    Query → Semantic Search → Retrieved Docs → Context → LLM Prompt → Response
    """
    
    # RAG Prompt Template
    rag_prompt = ChatPromptTemplate.from_template(
        """You are a helpful AJ Creations Shopping Assistant created by AiSyncBot.
        Here is the relevant store information:
        {context}
        User's question (Hinglish): {question}
        Guidelines:
        - Reply in English and Hinglish
        - Be friendly and helpful
        - Keep answers short and accurate (under 30 words)
        - If information is not in context, say "Store Ki Taraf se ye jankari Nahi hai."
        - Never mention OpenAI or other AI providers
        - Use the provided context to answer accurately
        Answer:
        """
    )
    
    # Chain: Retriever → Format → Prompt → LLM
    rag_chain = (
        {
            "context": lambda x: format_context(
                retrieval.semantic_search(x["question"])
            ),
            "question": lambda x: x["question"]
        }
        | rag_prompt
        | llm
    )
    
    return rag_chain


# Initialize RAG chain
rag_chain = create_rag_chain()


@router.post("/message", response_model=ChatMessageOutput)
async def chat_message(payload: ChatMessageInput):
    """
    Enhanced chat endpoint with RAG and Agent Tools integration.
    
    Flow:
    1. Detect user intent (RAG vs Tool)
    2. Route to appropriate handler:
       - RAG: General questions, FAQs, policies
       - Tools: Product search, cart, orders
    3. Extract structured data and return response
    """
    user_id_str = payload.user_id.strip()
    user_message = payload.message.strip()
    
    # Convert user_id to integer if possible (for authenticated users)
    user_id_int = None
    try:
        user_id_int = int(user_id_str)
    except (ValueError, TypeError):
        # If not an integer, it's an anonymous user with a string ID
        pass
    
    try:
        logger.info(f"💬 User {user_id_str}: {user_message}")
        
        # Create user chat history if it doesn't exist
        if user_id_str not in user_histories:
            user_histories[user_id_str] = ChatMessageHistory()
        
        history = user_histories[user_id_str]
        
        # Initialize response variables
        reply_text = ""
        tool_name = None
        products_data = None
        cart_data = None
        order_data = None
        sources = None
        
        # 1️⃣ DETECT INTENT USING LLM
        intent_data = detect_intent_with_llm(user_message)
        logger.info(f"🤖 LLM Intent Analysis: {intent_data}")
        
        # 2️⃣ ROUTE TO APPROPRIATE HANDLER
        if intent_data['should_use_tool'] and intent_data['tool_name']:
            # AGENT TOOL EXECUTION
            tool_name = intent_data['tool_name']
            logger.info(f"🔧 Executing tool: {tool_name}")
            
            # Prepare tool parameters from LLM output
            tool_params = extract_tool_parameters(tool_name, user_message, intent_data.get('parameters', {}))
            
            # Add user_id to cart/order tools
            if tool_name in ['view_cart', 'remove_from_cart', 'clear_cart', 'add_to_cart',
                               'list_orders', 'track_order', 'create_order']:
                # Use authenticated user_id if available, otherwise default to 1
                tool_params['user_id'] = user_id_int if user_id_int else 1
                logger.info(f"📊 Using user_id={tool_params['user_id']} for {tool_name}")
            
            # Execute tool
            tool_result = tool_registry.execute_tool(tool_name, **tool_params)
            
            # Format tool result into natural language response
            reply_text = format_tool_response(tool_name, tool_result, user_message)
            sources = [f"Tool: {tool_name}"]
            
            # ✅ NEW: Extract structured data from tool result
            if tool_name == 'search_products' and tool_result.get('success'):
                products = tool_result.get('products', [])
                products_data = [
                    ProductData(
                        name=p['name'],
                        price=p['price'],
                        description=p['description'],
                        rating=p.get('rating'),
                        stock=p.get('stock'),
                        product_id=p.get('sku', p.get('product_id'))
                    )
                    for p in products
                ]
                logger.info(f"✅ Extracted {len(products_data)} products")
            
            elif tool_name == 'view_cart' and tool_result.get('success'):
                items = tool_result.get('cart_items', [])
                if items:
                    cart_items = [
                        CartItemData(
                            product_name=item['product_name'],
                            quantity=item['quantity'],
                            price=item['price']
                        )
                        for item in items
                    ]
                    cart_data = CartSummary(
                        items=cart_items,
                        total=tool_result.get('total_price', 0),
                        total_items=len(items)
                    )
                    logger.info(f"✅ Cart has {len(cart_items)} items")
            
            elif tool_name == 'track_order' and tool_result.get('success'):
                order_data = OrderData(
                    order_id=tool_result.get('order_id', ''),
                    status=tool_result.get('status', 'Pending'),
                    estimated_delivery=tool_result.get('estimated_delivery', 'N/A'),
                    tracking_id=tool_result.get('tracking_id'),
                    order_date=tool_result.get('order_date')
                )
                logger.info(f"✅ Order tracking data extracted")
        
        else:
            # RAG PIPELINE for general questions
            logger.info("🔍 Using RAG pipeline for general question")
            
            # Semantic search
            retrieved_docs = retrieval.semantic_search(user_message)
            context = format_context(retrieved_docs)
            sources = [doc.metadata.get('source', 'unknown') for doc in retrieved_docs]
            
            logger.info(f"✅ Found {len(retrieved_docs)} relevant documents")
            
            # RAG chain
            response = rag_chain.invoke({"question": user_message})
            reply_text = response.content.strip()
        
        logger.info(f"✅ Response generated: {reply_text[:100]}...")
        
        # 3️⃣ STORE IN HISTORY
        history.add_message(HumanMessage(content=user_message))
        history.add_message(AIMessage(content=reply_text))
        
        # 4️⃣ RETURN RESPONSE WITH STRUCTURED DATA
        return ChatMessageOutput(
            user_id=user_id_str,
            message=user_message,
            reply=reply_text,
            tool_name=tool_name,
            products=products_data,
            cart=cart_data,
            order=order_data,
            timestamp=datetime.now(),
            sources=sources
        )
    
    except Exception as e:
        logger.error(f"❌ Error in chat_message: {e}", exc_info=True)
        return ChatMessageOutput(
            user_id=user_id_str,
            message=user_message,
            reply="क्षमा करें, मुझे आपके सवाल का जवाब देने में समस्या हो रही है।",
            timestamp=datetime.now(),
            sources=None
        )


def format_tool_response(tool_name: str, tool_result: dict, user_message: str) -> str:
    """
    Format tool execution result into natural language response.
    
    Args:
        tool_name: Name of the executed tool
        tool_result: Tool execution result
        user_message: Original user message
        
    Returns:
        Natural language response
    """
    if not tool_result.get('success'):
        return f"Sorry, I couldn't complete that action. {tool_result.get('error', '')}"
    
    # Product search
    if tool_name == 'search_products':
        products = tool_result.get('products', [])
        if not products:
            return "I couldn't find any products matching your search. Could you try different keywords?"
        
        response = f"I found {len(products)} products for you:\n\n"
        for i, product in enumerate(products, 1):
            response += f"{i}. **{product['name']}** - ₹{product['price']}\n"
            response += f"   {product['description']}\n"
            response += f"   Rating: {'⭐' * int(product.get('rating', 0))}\n\n"
        response += "Would you like to add any of these to your cart?"
        return response
    
    # List categories
    elif tool_name == 'list_categories':
        categories = tool_result.get('categories', [])
        response = "We have the following categories:\n\n"
        for cat in categories:
            response += f"• **{cat['display_name']}** ({cat['product_count']} items)\n"
        response += "\nWhat would you like to explore?"
        return response
    
    # View cart
    elif tool_name == 'view_cart':
        if tool_result.get('total_items', 0) == 0:
            return "Your cart is empty. Browse our products and add items you like!"
        
        items = tool_result.get('cart_items', [])
        response = f"Your cart has {tool_result['total_items']} items:\n\n"
        for item in items:
            response += f"• {item['product_name']} x{item['quantity']} - ₹{item['price'] * item['quantity']}\n"
        response += f"\n**Total: ₹{tool_result['total_price']}**\n"
        response += "\nReady to checkout?"
        return response
    
    # Add to cart
    elif tool_name == 'add_to_cart':
        return tool_result.get('message', 'Product added to cart!')
    
    # Remove from cart
    elif tool_name == 'remove_from_cart':
        return tool_result.get('message', 'Product removed from cart!')
    
    # Clear cart
    elif tool_name == 'clear_cart':
        return tool_result.get('message', 'Cart cleared!')
    
    # List orders
    elif tool_name == 'list_orders':
        orders = tool_result.get('orders', [])
        if not orders:
            return "You haven't placed any orders yet. Start shopping!"
        
        response = f"Your recent orders:\n\n"
        for order in orders[:5]:
            response += f"• Order #{order['order_id']} - ₹{order['total_price']}\n"
            response += f"  Status: {order['status']} | Date: {order['order_date'][:10]}\n\n"
        return response
    
    # Track order
    elif tool_name == 'track_order':
        tracking = tool_result.get('tracking_updates', [])
        response = f"Order #{tool_result.get('order_id')} Tracking:\n\n"
        for update in tracking:
            response += f"✓ {update['status']} - {update['location']}\n"
        response += f"\nEstimated delivery: {tool_result.get('estimated_delivery')}"
        return response
    
    # Default
    return tool_result.get('message', 'Action completed successfully!')


@router.get("/search")
async def search_documents(
    query: str = Query(..., min_length=1, description="Search query"),
    k: int = Query(3, ge=1, le=10, description="Number of results")
):
    """
    Direct semantic search endpoint
    
    Args:
        query: User's search query
        k: Number of results to return
    
    Returns:
        List of semantically relevant documents
    """
    try:
        logger.info(f"🔍 Search query: {query}")
        
        retrieval_instance = Retrieval(k=k)
        results = retrieval_instance.semantic_search(query)
        
        formatted_results = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "source": doc.metadata.get('source', 'unknown')
            }
            for doc in results
        ]
        
        logger.info(f"✅ Found {len(formatted_results)} results")
        
        return {
            "query": query,
            "results_count": len(formatted_results),
            "results": formatted_results,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"❌ Search error: {e}", exc_info=True)
        return {
            "query": query,
            "results_count": 0,
            "results": [],
            "status": "error",
            "message": str(e)
        }


@router.get("/chat-history/{user_id}")
async def get_chat_history(user_id: str):
    """Get chat history for a user"""
    try:
        if user_id not in user_histories:
            return {"user_id": user_id, "history": [], "message": "No history found"}
        
        history = user_histories[user_id]
        
        formatted_history = [
            {
                "type": msg.__class__.__name__,
                "content": msg.content
            }
            for msg in history.messages
        ]
        
        return {
            "user_id": user_id,
            "history": formatted_history,
            "message_count": len(formatted_history)
        }
    
    except Exception as e:
        logger.error(f"❌ Error getting history: {e}")
        return {"error": str(e), "status": "failed"}


@router.delete("/chat-history/{user_id}")
async def clear_chat_history(user_id: str):
    """Clear chat history for a user"""
    try:
        if user_id in user_histories:
            del user_histories[user_id]
            return {"status": "success", "message": f"History cleared for {user_id}"}
        return {"status": "not_found", "message": f"No history for {user_id}"}
    
    except Exception as e:
        logger.error(f"❌ Error clearing history: {e}")
        return {"error": str(e), "status": "failed"}
