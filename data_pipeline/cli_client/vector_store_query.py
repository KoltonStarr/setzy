import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from data_pipeline.logger import log
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# This connects to existing store - does NOT create new one
vector_store = Chroma(
    collection_name="sales_calls",
    embedding_function=embeddings,
    persist_directory="../vector_store"
)

log("What would you ike to search for?", "white")
search_query = input("> ")

log("How many k-nearest-neighbors do you want?", "white")
k_value = int(input("> "))

results = vector_store.similarity_search(
    f"{search_query}",
    k=k_value
)

print(results)