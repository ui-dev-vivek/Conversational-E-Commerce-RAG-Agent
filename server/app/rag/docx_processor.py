from langchain_community.document_loaders import PyPDFLoader #(pypdf)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document

class DocxProcessor:
    def __init__(self, file_path: List,chunk_size: int = 300, chunk_overlap: int = 50):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )
    def procces_pdf(self) -> List[Document]:
        chunks=[]
        #First Here Load The Documents
        for file in self.file_path:
            loader=PyPDFLoader(file)
            documents=loader.load()
            #Split Documnets into Chunks  
            chunk=self.splitter.split_documents(documents)
            chunks.extend(chunk)
        return chunks #return Chunks
        
        
       