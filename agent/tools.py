import os
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from typing import Optional

# A search tool for the vector database. 
@tool 
def vector_search(query: str, k_value: int, filters: Optional[dict]) -> list[Document]:
    """Gets relevant data from a vector store to adequately answer a query.
    
    Args:
        query (str): The query that will be used to get relevant data from the vector store.
        k_value (int): Number of k-nearest neighbors
        vector_store (Chroma): A full chroma instance.
        filters: metadata filters for the query to the vector store.
    
    Returns:
        list[Document]
    """
    vector_store = Chroma(
        collection_name="sales_calls",
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
        persist_directory=os.getenv("VECTOR_STORE_PERSIST_DIRECTORY"),
    )
    return vector_store.similarity_search(query, k=k_value, filter=filters)


# A tool to read the embedding pipeline code if needed. 
# A websearch tool.