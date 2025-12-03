from system_prompt import SYSTEM_PROMPT
from tools import vector_search, web_search
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

agent = create_agent(init_chat_model("gpt-5"), tools=[vector_search, web_search], system_prompt=SYSTEM_PROMPT)

print("What would you like to search for?")
user_query = input("> ")

for event in agent.stream(
    {"messages": [{"role": "user", "content": user_query}]},
    stream_mode="values",
):
    event["messages"][-1].pretty_print()