from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from logger import log
import chromadb
import os

class VectorStore:
    @staticmethod
    def create_store() -> Chroma:
        # Connect to remote ChromaDB server
        chroma_client = chromadb.HttpClient(
            host=os.getenv("CHROMADB_HOST", "localhost"),
            port=int(os.getenv("CHROMADB_PORT", "8000"))
        )

        return Chroma(
            client=chroma_client,
            collection_name="sales_calls",
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
        )
    
    @staticmethod
    def is_already_embedded(vector_store, call_identifier) -> bool:
        print(call_identifier)
        existing_docs = vector_store.get(
            where={"call_identifier": call_identifier},
            limit=1
        )

        if existing_docs['ids']:
            log(f"Skipping {call_identifier} - already embedded in vector store", "blue")
            return True
        else:
            return False 
    
