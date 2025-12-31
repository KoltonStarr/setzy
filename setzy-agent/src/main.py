from system_prompt import SYSTEM_PROMPT
from logger import log, log_agent_msg
from tools import vector_search, web_search
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import ToolMessage, AIMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()

max_iterations = 5
agent = create_agent(
    init_chat_model("gpt-5"), 
    tools=[vector_search, web_search], 
    system_prompt=SYSTEM_PROMPT
)

print("Type q to quit at any time.")
print("How can I help you?")
messages = []

iteration = 1
while iteration <= 5:
    # Get the user's input.
    user_query = input("> ")
    messages.append({"role": "user", "content": user_query})
    if user_query == "q":
        break
    
    last_event = None
    for event in agent.stream({"messages": messages}, stream_mode="values"):
        last_event = event 
        # Every event carries all previous messages.
        msg: ToolMessage | AIMessage | HumanMessage = event["messages"][-1]

        log_agent_msg(msg)

    # At this point. All events are done emitting. The last_event will contain the last event that was emitted.
    # That event should have ALL the messages needed for the next run. Context should be set.
    messages = last_event["messages"]
    iteration += 1

log("Goodbye!!")