"""Embedding generation for products and FAQs."""
from typing import List


class Embedder:
    """Generate embeddings using sentence-transformers."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        # TODO: Initialize sentence-transformers model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        # TODO: Implement embedding generation
        return []

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query."""
        # TODO: Implement query embedding
        return []
