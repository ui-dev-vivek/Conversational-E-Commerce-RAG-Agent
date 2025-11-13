"""
RAG (Retrieval-Augmented Generation) Module
Handles embeddings, vector stores, and document processing
"""

from .embeddings.local_embedder import LocalEmbedder
from .vectorstore.chroma_store import ChromaStore
from .json_processor import JsonProcessor
from .docx_processor import DocxProcessor

__all__ = [
    "LocalEmbedder",
    "ChromaStore",
    "JsonProcessor",
    "DocxProcessor",
    "ChromaStore.vectorstore",
    "LocalEmbedder.embeddings"
]

__version__ = "1.0.0"