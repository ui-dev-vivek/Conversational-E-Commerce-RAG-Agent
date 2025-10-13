from fastapi import APIRouter
from pydantic import BaseModel
import time

router = APIRouter()


class ChatMessage(BaseModel):
    message: str


@router.post("/message")
async def chat_message(payload: ChatMessage):
    user_message = payload.message
    time.sleep(1)
    # TODO: Integrate RAG + LLM here
    # For now, echo the message back
    bot_reply = f"I received your message.   How can I help you with our products?"
    
    return {"reply": bot_reply}

