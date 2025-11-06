# Abstract base class for LLM implementations
# Defines interface for LLM invocation and streaming
from langchain_openai import ChatOpenAI
from ...config.llm_config import llm_config
class BaseLlm:
    def __init__(self):
        self.key = llm_config.API_KEY
        if not self.key:
            raise ValueError(f"{llm_config.PROVIDER.upper()}_API_KEY is not set. Please set it in the .env file or environment variables.")
        self.model = llm_config.MODEL
        self.llm = ChatOpenAI(
            model=self.model,
            openai_api_key=self.key,
            openai_api_base=llm_config.API_BASE,
            temperature=0.7
        )
    