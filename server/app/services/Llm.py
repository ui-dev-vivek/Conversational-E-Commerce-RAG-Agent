#LLM to get Generative Responses.
from langchain_openai import ChatOpenAI


class Llm:
    def __init__(self):
        self.key="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"
        self.llm = ChatOpenAI(
            model="openai/gpt-oss-20b:free",
            api_key=self.key,
            base_url="https://openrouter.ai/api/v1",
            temperature=0.7
        )
        

