## To Do (Agent)
- I need to configure the agent to be thread aware. 
--- I need to create the chat POST endpoint with FastAPI.
--- Have a dictionary for messages where the key is the thread_id. 
--- If the thread_id is nil or None then create a new thread_id and write it to the dict with the first user msg.
--- If the thread_id is provided then look it up. Error if cannot find.
--- If thread_id is found then ALL messages are now available.
--- Parse out the new message from the body and add it as a user message to the found list of messages.
--- Kick of the agent with the list of messages.
--- Get the return message from the agent, make sure it goes into the dict. 
--- Return the agents final message to the user. 


- Allow the agent to be accessed via an API or remote call. 
-- Look into using FastAPI to create an HTTP layer around the agent.
-- The endpoint should accept a single user prompt as the main parameter / body. 
-- The endpoint should only return the answer that is due the user. What the client decides to do with all of 
the back and forth is up to the client. But the endpoint will only accept the one query. 
-- The agent will obviously be taking the individual queries and remembering them in-memory so that an 
adequate flow of back-and-forth can occur. 

- Make the system prompt more configurable and dynamic (call phases, type of call) and have that flow into the chunking and 
embedding process. This way other orgs can ensure that their calls are understood by the agent in a way that is specific to them.

## To Do (Data Pipeline)
- Refactor the data pipeline to be a long-running process that polls an SQS queue for new audio files to embed. 
- Refactor the data pipeline to process 10 calls at once with two concurrent threads (5 each thread) then start another batch until all
have been processed.
- Refactor the data pipeline to clear out the data dir and transcripts dir when a batch is done.

## To Do (Engineering)
- Architect and implement a solution for uploading calls to S3 and then kicking off a mesasge to SQS.
- Add CloudFormation templates for S3 bucket and SQS queue.

╰─$ poetry env activate   
╰─$ eval $(poetry env activate)

## Readings
- Poetry
- ChromaDB
- Pydantic 
- LangGraph MemorySaver