import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from logger import log
from dotenv import load_dotenv
load_dotenv()
    
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Connect to remote ChromaDB server
chroma_client = chromadb.HttpClient(
    host=os.getenv("CHROMADB_HOST", "localhost"),
    port=int(os.getenv("CHROMADB_PORT", "8000"))
)

vector_store = Chroma(
    client=chroma_client,
    collection_name="sales_calls",
    embedding_function=embeddings,
)

log("What would you ike to search for?", "white")
search_query = input("> ")

log("How many k-nearest-neighbors do you want?", "white")
k_value = int(input("> "))

documents = vector_store.similarity_search(
    f"{search_query}",
    k=k_value
)

for doc in documents:
    log(f"Type: {doc.metadata['type']}")
    log(f"Source: {doc.metadata['call_identifier']}")
    log("-----------------------", "blue")