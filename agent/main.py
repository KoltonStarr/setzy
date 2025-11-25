import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
# ===
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
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

model = init_chat_model("gpt-4.1")

@tool(response_format="content_and_artifact")
def retrieve_context(query: str, k: int):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

tools = [retrieve_context]
# If desired, specify custom instructions
prompt = (
    "You have access to a tool that retrieves context from setter call data. "
    "Use the tool to help answer user queries."
)
agent = create_agent(init_chat_model("gpt-4.1"), tools, system_prompt=prompt)

query = (
    "How many times does the word 'um' appear across all calls?"
)

for event in agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    event["messages"][-1].pretty_print()