from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

from system_prompt import SYSTEM_PROMPT
from logger import log_agent_msg
from tools import vector_search, web_search
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import ToolMessage, AIMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()

class ChatMessage(BaseModel):
    message: str
    thread_id: str | None = None

app = FastAPI()

# Global memory.
all_messages: dict[str, list] = {}

# Instantiate Agent.
agent = create_agent(
    init_chat_model("gpt-5"), 
    tools=[vector_search, web_search], 
    system_prompt=SYSTEM_PROMPT
)

@app.post("/chat")
async def chat(incomingMessage: ChatMessage) -> ChatMessage:
    thread_id = incomingMessage.thread_id
    user_query = {"role": "user", "content": incomingMessage.message}

    # Case: First time chat or totally new chat. Initialize thread.
    if not thread_id:
        thread_id = str(uuid4())
        all_messages[thread_id] = []
    
    all_messages[thread_id].append(user_query)

    # Thread message will be either:
    # -- A list with a single user query object (first time prompt.)
    # -- A list with several human, ai, and tool call messages with the last message being the most recent user query.
    thread_messages = all_messages[thread_id]

    # Ready to start agent.
    last_event = None
    for event in agent.stream({"messages": thread_messages}, stream_mode="values"):
        last_event = event 
        # Every event carries all previous messages.
        msg: ToolMessage | AIMessage | HumanMessage = event["messages"][-1]

        log_agent_msg(msg)

    # At this point. All events are done emitting. The last_event will contain the last event that was emitted.
    # That event should have ALL the messages needed for the next run. Context should be set.
    all_messages[thread_id] = last_event["messages"]

    # Get the most recent message (ai response)
    ai_response = all_messages[thread_id][-1].content

    return ChatMessage(thread_id=thread_id, message=ai_response)