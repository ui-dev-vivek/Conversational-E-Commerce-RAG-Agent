from langchain_openai import ChatOpenAI
from .settings import settings
import random

class LLMConfig:
    PROVIDER: str = settings.llm_provider
    
    def __init__(self):
        switcher = {
            'openrouter': self._configure_openrouter,
            'openai': self._configure_openai,
            'anthropic': self._configure_anthropic,
        }
        switcher.get(self.PROVIDER, lambda: None)()

    def _configure_openrouter(self):
        self.models = settings.openrouter_models.split('|') if settings.openrouter_models else []
        self.api_keys = settings.openrouter_api_keys.split('|') if settings.openrouter_api_keys else []
        self.API_BASE = settings.openrouter_api_base
        self.MODEL = random.choice(self.models) if self.models else None
        self.API_KEY = random.choice(self.api_keys) if self.api_keys else None

    def _configure_openai(self):
        self.MODEL = settings.openai_model
        self.API_KEY = settings.openai_api_key
        self.API_BASE = settings.openai_api_base

    def _configure_anthropic(self):
        self.MODEL = settings.anthropic_model
        self.API_KEY = settings.anthropic_api_key
        self.API_BASE = settings.anthropic_api_base
    def invoke(self):
        return ChatOpenAI(
            model=self.MODEL,
            openai_api_key=self.API_KEY,
            openai_api_base=self.API_BASE,
            temperature=0.7
        )
        
LLM = LLMConfig()
