from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from app.config.settings import settings

class LocalEmbedder:
    def __init__(self):
        self.model_name=settings.huggingface_embedding_model
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    # Not Used 
    def embed_documents(self,documents:List[str]):
        return self.embeddings.embed_documents(documents)   
        # self.embeddings.embed_query(query) if text
    def embed_query(self,query:str):
        return self.embeddings.embed_query(query)