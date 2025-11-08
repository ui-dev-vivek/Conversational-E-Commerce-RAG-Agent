from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from app.config.settings import settings
class Embedder:
    def __init__(self):
        self.model_name=settings.huggingface_embedding_model
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
 