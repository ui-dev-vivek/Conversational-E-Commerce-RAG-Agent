from pydentic import BaseModel
from typing import Optional, List


class LoginRequest(BaseModel):
    email: str
    password: str
 
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str
    user_id: int
    expired_at: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str]
    
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]