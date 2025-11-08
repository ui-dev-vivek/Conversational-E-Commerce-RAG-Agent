import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag.docx_processor import DocxProcessor

docs = DocxProcessor(['./data/documents/store_guid.pdf'])
chunks = docs.procces_pdf()
print(chunks[0])