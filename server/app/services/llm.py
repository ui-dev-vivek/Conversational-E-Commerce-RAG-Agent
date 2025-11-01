from langchain_openai import ChatOpenAI
import os
from ..config.settings import settings


class Llm:
    def __init__(self):
        self.key = settings.openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.key:
            raise ValueError("OPENROUTER_API_KEY is not set. Please set it in the .env file or environment variables.")

        self.executor = ChatOpenAI(
            model="openai/gpt-oss-20b:free",
            openai_api_key=self.key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.7
        )
