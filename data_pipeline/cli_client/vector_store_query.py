import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
from logger import log
from dotenv import load_dotenv
load_dotenv()
    
persist_directory = os.getenv("VECTOR_STORE_PERSIST_DIRECTORY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(
    collection_name="sales_calls",
    embedding_function=embeddings,
    persist_directory=persist_directory,  # Where to save data locally, remove if not necessary
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
    print(f"Type: {doc.metadata['type']}")
    print(f"Source: {doc.metadata['call_identifier']}")