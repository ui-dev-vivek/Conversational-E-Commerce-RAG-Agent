from langchain_community.document_loaders import JSONLoader #(jq)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document

class JsonProcessor:
    def __init__(self, file_path: List,chunk_size: int = 300, chunk_overlap: int = 50):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )
    def procces_json(self) -> List[Document]:
        chunks=[]
        #First Here Load The Documents
        for file in self.file_path:
            loader=JSONLoader(
                file_path=file,
                jq_schema=".",
                text_content=False,
            )
            documents=loader.load()
            #Split Documnets into Chunks  
            chunk=self.splitter.split_documents(documents)
            chunks.extend(chunk)
        return chunks #return Chunks
        
        
       