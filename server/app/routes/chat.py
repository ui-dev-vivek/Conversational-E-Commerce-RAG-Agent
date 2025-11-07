from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from ..config.llm_config import LLM

router = APIRouter()
llm = LLM.invoke()

# Simple per-user in-memory store
user_histories = {}


class ChatMessage(BaseModel):
    user_id: str 
    message: str


@router.post("/message")
async def chat_message(payload: ChatMessage):
    """Handles chat messages and stores conversation per user."""
    user_id = payload.user_id.strip()
    user_message = payload.message.strip()
  
    # Create user chat history if it doesn't exist
    if user_id not in user_histories:
        user_histories[user_id] = ChatMessageHistory()

    history = user_histories[user_id]
   
    # System instructions (persona definition)
    system_message = SystemMessage(
        content=(
            "You are the Flipkart Shopping Assistant created by AiSyncBot. "
            "Speak in a friendly, helpful, and concise tone like a real store helper. "
            "Never mention OpenAI or any AI provider. "
            "Keep answers short (under 30 words) and accurate about products or shopping help."
            "User ask in Hinglish. You reply in Hindi."
        )
    )    
    # Add system and user messages
    history.add_message(system_message)
    history.add_message(HumanMessage(content=user_message))
    
    # Call LLM with full message context
    response = await llm.ainvoke(history.messages)
    
    reply_text = response.content.strip()
    # Add assistant message to memory
    history.add_message(AIMessage(content=reply_text))
    return {"reply": reply_text}
