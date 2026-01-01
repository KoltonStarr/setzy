## To Do (Agent)
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