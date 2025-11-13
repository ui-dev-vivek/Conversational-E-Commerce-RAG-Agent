import sys
from pathlib import Path

# # Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from app.services.rag.retrieval import Retrieval
# from app.rag import JsonProcessor,LocalEmbedder,DocxProcessor
# # from app.rag.embeddings.local_embedder import LocalEmbedder
# docs = JsonProcessor(['./data/faqs.json','./data/products.json'])
# json_data = docs.procces_json()
# chunks = [doc.page_content for doc in json_data[1:3]]

# embedder = LocalEmbedder()
# embeddings = embedder.embed_query(chunks[0])
# print(embeddings)
# # print(json_data)

retrieval = Retrieval()
query = "What is the price of Elegant Cotton Kurti?"
result = retrieval.semantic_search(query)
print(result)