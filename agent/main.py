import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
# ===
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from system_prompt import SYSTEM_PROMPT
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

# Connect to existing vector store.
vector_store = Chroma(
    collection_name="sales_calls",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory=os.getenv("VECTOR_STORE_PERSIST_DIRECTORY"),
)

agent = create_agent(init_chat_model("gpt-4.1"), tools=[], system_prompt=SYSTEM_PROMPT)

print("What would you like to search for?")
user_query = input("> ")

for event in agent.stream(
    {"messages": [{"role": "user", "content": user_query}]},
    stream_mode="values",
):
    event["messages"][-1].pretty_print()