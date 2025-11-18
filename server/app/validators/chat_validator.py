from pydantic import BaseModel

class ChatMessageInput(BaseModel):
    user_id: str 
    message: str

class ChatMessageOutput(BaseModel):    
    reply: str