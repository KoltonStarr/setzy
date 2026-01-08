import os
import chromadb
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from typing import Optional
from langchain_community.tools import DuckDuckGoSearchRun

# Web search tool (free, no API key needed)
web_search = DuckDuckGoSearchRun()

# A search tool for the vector database. 
@tool 
def vector_search(query: str, k_value: int, filters: Optional[dict]) -> list[Document]:
    """Gets relevant data from a vector store to adequately answer a query.
    
    Args:
        query (str): The query that will be used to get relevant data from the vector store.
        k_value (int): Number of k-nearest neighbors
        vector_store (Chroma): A full chroma instance.
        filters: metadata filters for the query to the vector store.
            For single conditions: {"type": "full_transcript"}
            For multiple conditions: {"$and": [{"type": "sliding_window_chunk"}, {"call_identifier": "xyz"}]}
            IMPORTANT: Only use $and or $or with TWO OR MORE conditions. Single conditions must be passed as a dict without operators.
    
    Returns:
        list[Document]
    """
    # Connect to remote ChromaDB server
    chroma_client = chromadb.HttpClient(
        host=os.getenv("CHROMADB_HOST", "localhost"),
        port=int(os.getenv("CHROMADB_PORT", "8000"))
    )
    
    vector_store = Chroma(
        client=chroma_client,
        collection_name="sales_calls",
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    )
    return vector_store.similarity_search(query, k=k_value, filter=filters)