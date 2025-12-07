from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from datetime import datetime
import logging
import re

from ..config.llm_config import LLM
from ..validators.chat_validator import ChatMessageInput, ChatMessageOutput
from ..services.rag.retrieval import Retrieval
from ..agents.tools.tool_registry import tool_registry

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


def detect_intent(message: str) -> dict:
    """
    Detect user intent from message to route to appropriate handler.
    
    Returns:
        dict with 'type' (rag/tool) and 'tool_name' if applicable
    """
    message_lower = message.lower()
    
    # Product search intents - IMPROVED
    if any(word in message_lower for word in ['search', 'find', 'show', 'looking for', 'want', 'need', 'dhundo', 'dikhao']):
        # Generic product query - show all products
        if any(word in message_lower for word in ['product', 'products', 'item', 'items', 'all', 'everything']):
            return {'type': 'tool', 'tool_name': 'search_products', 'query': message}
        # Specific product search
        elif any(word in message_lower for word in ['kurti', 'saree', 'candle', 'soap', 'cosmetic', 'dress', 'cotton', 'lavender']):
            return {'type': 'tool', 'tool_name': 'search_products', 'query': message}
    
    # Category listing
    if any(word in message_lower for word in ['categories', 'category', 'types', 'what do you sell', 'kya hai']):
        return {'type': 'tool', 'tool_name': 'list_categories'}
    
    # Cart operations
    if 'cart' in message_lower:
        if any(word in message_lower for word in ['add', 'put', 'daalo']):
            return {'type': 'tool', 'tool_name': 'add_to_cart'}
        elif any(word in message_lower for word in ['remove', 'delete', 'hatao']):
            return {'type': 'tool', 'tool_name': 'remove_from_cart'}
        elif any(word in message_lower for word in ['show', 'view', 'see', 'dikhao', 'check']):
            return {'type': 'tool', 'tool_name': 'view_cart'}
        elif any(word in message_lower for word in ['clear', 'empty', 'khali']):
            return {'type': 'tool', 'tool_name': 'clear_cart'}
    
    # Order operations
    if any(word in message_lower for word in ['order', 'orders']):
        if any(word in message_lower for word in ['track', 'where', 'status', 'kaha', 'delivery']):
            return {'type': 'tool', 'tool_name': 'track_order'}
        elif any(word in message_lower for word in ['list', 'show', 'my', 'history', 'dikhao']):
            return {'type': 'tool', 'tool_name': 'list_orders'}
    
    # Default to RAG for general questions
    return {'type': 'rag'}


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
    3. Get response and store in history
    """
    user_id = payload.user_id.strip()
    user_message = payload.message.strip()
    
    try:
        logger.info(f"💬 User {user_id}: {user_message}")
        
        # Create user chat history if it doesn't exist
        if user_id not in user_histories:
            user_histories[user_id] = ChatMessageHistory()
        
        history = user_histories[user_id]
        
        # 1️⃣ DETECT INTENT
        intent = detect_intent(user_message)
        logger.info(f"🎯 Detected intent: {intent}")
        
        # 2️⃣ ROUTE TO APPROPRIATE HANDLER
        if intent['type'] == 'tool':
            # AGENT TOOL EXECUTION
            tool_name = intent['tool_name']
            logger.info(f"🔧 Executing tool: {tool_name}")
            
            # Prepare tool parameters based on tool type
            tool_params = {}
            
            # Product tools don't need user_id
            if tool_name == 'search_products':
                # Extract keywords from natural language query
                keywords = extract_keywords(user_message)
                tool_params['query'] = keywords
                tool_params['limit'] = 5
                logger.info(f"🔍 Extracted keywords: '{keywords}' from '{user_message}'")
            elif tool_name == 'list_categories':
                pass  # No parameters needed
            elif tool_name == 'get_product_details':
                # Extract product ID from message if present
                tool_params['product_id'] = user_message
            # Cart and order tools need user_id (integer from database)
            elif tool_name == 'add_to_cart':
                # Extract product name from message
                # "Add Printed Palazzo Set to cart" -> "Printed Palazzo Set"
                from app.config.database import SessionLocal
                from app.models.models import Product
                
                # Try to extract product name
                message_lower = user_message.lower()
                # Remove common words
                product_name = user_message
                for word in ['add', 'to', 'cart', 'put', 'daalo', 'please']:
                    product_name = product_name.replace(word, '').replace(word.title(), '')
                product_name = product_name.strip()
                
                # Search for product in database
                db = SessionLocal()
                try:
                    product = db.query(Product).filter(
                        Product.name.ilike(f"%{product_name}%")
                    ).first()
                    
                    if product:
                        tool_params['user_id'] = 1  # Default user
                        tool_params['product_id'] = product.sku
                        tool_params['quantity'] = 1
                        logger.info(f"🛒 Found product: {product.name} (SKU: {product.sku})")
                    else:
                        # Product not found, return error
                        logger.warning(f"⚠️ Product not found: {product_name}")
                        tool_result = {
                            "success": False,
                            "message": f"Sorry, I couldn't find '{product_name}' in our catalog. Please try searching for products first."
                        }
                        reply_text = format_tool_response(tool_name, tool_result, user_message)
                        sources = [f"Tool: {tool_name}"]
                        history.add_message(HumanMessage(content=user_message))
                        history.add_message(AIMessage(content=reply_text))
                        return ChatMessageOutput(
                            user_id=user_id,
                            message=user_message,
                            reply=reply_text,
                            sources=sources
                        )
                finally:
                    db.close()
                    
            elif tool_name in ['view_cart', 'remove_from_cart', 'clear_cart',
                               'get_order_status', 'list_orders', 'create_order', 'track_order']:
                # For now, use a default user ID (1 = test user)
                # In production, this should come from JWT token
                tool_params['user_id'] = 1  # Default to test user
            
            # Execute tool
            tool_result = tool_registry.execute_tool(tool_name, **tool_params)
            
            # Format tool result into natural language response
            reply_text = format_tool_response(tool_name, tool_result, user_message)
            sources = [f"Tool: {tool_name}"]
            
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
        
        # 4️⃣ RETURN RESPONSE
        return ChatMessageOutput(
            user_id=user_id,
            message=user_message,
            reply=reply_text,
            timestamp=datetime.now(),
            sources=sources
        )
    
    except Exception as e:
        logger.error(f"❌ Error in chat_message: {e}", exc_info=True)
        return ChatMessageOutput(
            user_id=user_id,
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
