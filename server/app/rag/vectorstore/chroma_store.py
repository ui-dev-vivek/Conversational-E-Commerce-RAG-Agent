from langchain_chroma import Chroma
from ..embeddings.local_embedder import LocalEmbedder
from ...config.settings import settings
embadder = LocalEmbedder()

class ChromaStore:
    def __init__(self,collection_name="products"):
        self.collection_name = collection_name
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embadder.embeddings,
            persist_directory=settings.chroma_db_path,
        )

    def add_documents(self,documents):
        self.vectorstore.add_documents(documents)

    def update_documents(self,ids,documents):
        self.vectorstore.update_documents(ids,documents)

    def delete_documents(self,ids):
        self.vectorstore.delete(ids)


