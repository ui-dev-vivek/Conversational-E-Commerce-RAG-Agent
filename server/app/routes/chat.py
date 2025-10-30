from fastapi import APIRouter
from pydantic import BaseModel
import time
from ..services.llm import Llm
# from langchain.prompts import PromptTemplate
router = APIRouter()

llm = Llm()

class ChatMessage(BaseModel):
    message: str


@router.post("/message")
async def chat_message(payload: ChatMessage):
    user_message = payload.message
    # time.sleep(1)
    message = "Your the Chat assistant,\n\n your name is Flipkart Shoping Assistant,  naver says OpenAI word if come to **, you are created by AiSyncBot. \n\n Assist to in 1 line to answer this question: " + user_message
    #bot_reply = f"I received your message: {user_message}.   How can I help you with our products?"
    print('started')
    langchain_output = llm.executor.invoke(message)
    print('completed')
    return {"reply": langchain_output.content}

