import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag.json_processor import JsonProcessor
from app.rag.docx_processor import DocxProcessor
# from app.rag.embeddings.local_embedder import LocalEmbedder
from app.rag.vectorstore.chroma_store import ChromaStore
def main():
    try:
        Json_docs = JsonProcessor(['./data/faqs.json','./data/products.json'])
        pdf_docs = DocxProcessor(['./data/documents/store_guid.pdf','./data/documents/store_information.pdf','./data/documents/store_policy.pdf'])
        pdf_data = pdf_docs.procces_pdf()
        json_data = Json_docs.procces_json()
        print(f"Total JSON Documents: {len(json_data)}")
        print(f"Total PDF Documents: {len(pdf_data)}")
        # embedder = LocalEmbedder()
        store = ChromaStore()
        print("Adding Documents to ChromaDB")
        store.add_documents(json_data)
        store.add_documents(pdf_data)
        print("Documents Added to ChromaDB")
    except Exception as e:
        print(f"Error Occurred: {e}")
if __name__ == "__main__":
    main()

