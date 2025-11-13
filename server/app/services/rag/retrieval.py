from app.rag import ChromaStore, LocalEmbedder
from typing import List, Dict, Any
from app.config.llm_config import LLM
from langchain_core.documents import Document

store = ChromaStore()
embeddings = LocalEmbedder()
class Retrieval:
    def __init__(self,k=4):
        self.vectorstore = store.vectorstore
        self.embedder = embeddings
        self.llm = LLM.invoke()
        self.k = k 
        
    def pre_retrive(self,query:str) -> Dict[str,Any]:
        #Extend Query with LLM
        prompt = f"Rephrase this search query to be semantically rich and specific:\n\n{query}"
        reformulated = self.llm.invoke(prompt).content.strip()
        embeddings = self.embedder.embed_query(reformulated) 
        return {"query":reformulated,"embeddings":embeddings,"raw_query":query}       
   
    def retrieve(self, query: str) -> Dict[str, Any]:
        results = self.vectorstore.similarity_search(query, k=self.k)
        return results
    def post_retrieval(self, query: str, docs: List[Document]) -> List[Document]:

        try:
            if not docs:
                return []

            prompt = f"""
                        You are an expert semantic reranker.
                        Given the query: "{query}"
                        Rank the following document chunks by how relevant they are.
                        Return a list of indexes (0-based) in descending order of relevance.

                        Documents:
                        {[d.page_content[:400] for d in docs]}
            """
            response = self.llm.invoke(prompt).content
            ranked_indices = self._parse_indices(response, len(docs))

            reranked_docs = [docs[i] for i in ranked_indices if i < len(docs)]
            return reranked_docs

        except Exception as e:            
            return docs

    def _parse_indices(self, text: str, n: int) -> List[int]:
        """Extract numeric indices from LLM output safely."""
        import re
        nums = re.findall(r'\d+', text)
        return [int(i) for i in nums if int(i) < n]


    def semantic_search(self, query: str) -> List[Document]:
        """
        Full semantic search pipeline (Pre + Retrieve + Post).
        """
        pre = self.pre_retrive(query)
        retrieved = self.retrieve(pre["query"])
        final_docs = self.post_retrieval(pre["raw_query"], retrieved)
        return final_docs