from fastapi import APIRouter

router = APIRouter()


@router.post("/message")
async def chat_message(message: str):
    # Placeholder: integrate RAG + LLM here
    return {"reply": f"Echo: {message}"}
