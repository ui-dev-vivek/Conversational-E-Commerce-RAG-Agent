from pydantic_settings import BaseSettings
from typing import Optional, Any

class Settings(BaseSettings):
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_name: Optional[str] = None
    debug: bool = False
    
    # LLM Configuration
    llm_provider: str = "openrouter"  # Default provider
    openai_api_key: Optional[str] = None
    openai_model: str = None
    openai_api_base: str = "https://api.openai.com/v1"
    
    openrouter_api_key: Optional[str] = None
    openrouter_api_keys: Optional[str] = None
    openrouter_models: Optional[str] = None
    openrouter_api_base: str = "https://openrouter.ai/api/v1"
    
    anthropic_api_key: Optional[str] = None
    anthropic_model: Optional[str] = None
    anthropic_api_base: Optional[str] = None
    
    huggingface_api_key: Optional[str] = None
    huggingface_embedding_model: Optional[str] = None
    
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow" 


# Create a singleton settings instance
settings = Settings()