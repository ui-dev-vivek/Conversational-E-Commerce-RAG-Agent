from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_name: Optional[str] = None
    debug: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # This allows extra fields