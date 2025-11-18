from fastapi import APIRouter, Query
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from datetime import datetime
import logging

from ..config.llm_config import LLM
from ..validators.chat_validator import ChatMessageInput, ChatMessageOutput
from ..services.rag.retrieval import Retrieval

logger = logging.getLogger(__name__)

router = APIRouter()
llm = LLM.invoke()
retrieval = Retrieval(k=3)

# Simple per-user in-memory store
user_histories = {}


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
    Chat endpoint with Semantic Search RAG Chain

    Flow:
    1. Get user message
    2. Semantic search for relevant documents
    3. Create context from documents
    4. Format prompt with context
    5. Get LLM response
    6. Store in chat history
    """
    user_id = payload.user_id.strip()
    user_message = payload.message.strip()

    try:
        logger.info(f"💬 User {user_id}: {user_message}")

        # Create user chat history if it doesn't exist
        if user_id not in user_histories:
            user_histories[user_id] = ChatMessageHistory()

        history = user_histories[user_id]

        # 1️⃣ SEMANTIC SEARCH - Retrieve relevant documents
        logger.info("🔍 Retrieving relevant documents...")
        retrieved_docs = retrieval.semantic_search(user_message)
        context = format_context(retrieved_docs)
        sources = [doc.metadata.get('source', 'unknown') for doc in retrieved_docs]

        logger.info(f"✅ Found {len(retrieved_docs)} relevant documents")

        # 2️⃣ RAG CHAIN - Process through LLM with context
        logger.info("🤖 Generating response with RAG chain...")
        response = rag_chain.invoke({"question": user_message})
        reply_text = response.content.strip()

        logger.info(f"✅ Response generated: {reply_text[:100]}...")

        # 3️⃣ STORE IN HISTORY
        history.add_message(SystemMessage(content=f"Context: {context}"))
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
