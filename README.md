## To Do (Agent)
- Make the system prompt more configurable and dynamic (call phases, type of call) and have that flow into the chunking and 
embedding process. This way other orgs can ensure that their calls are understood by the agent in a way that is specific to them.
-- The only change to the embedding pipeline would be the call phase chunker. I'm already using an LLM to DO the chunking task based on a prompt. So the bones of this functionality are already there. Just need to determine a way to allow the user to easily provide that prompt somehow. 
-- There needs to be sync between the call phases mentioned in the agent's prompt and the call phases mentioned in the data pipeline call phase chunker document. I need to combine them and make them shared somehow to cut down on redundancy.

## Nice-to-have
- Add configuration to control the size of the agent's memory. Add code to clear message history when memory limit has been reached. 
- Protect the endpoint with oauth / STS connection.

## To Do (Data Pipeline)
- Convert to Poetry
- Refactor the data pipeline to be a long-running process that polls an SQS queue for new audio files to embed. 
- Refactor the data pipeline to process 10 calls at once with two concurrent threads (5 each thread) then start another batch until all
have been processed.
- Refactor the data pipeline to clear out the data dir and transcripts dir when a batch is done.

## To Do (Backend)
- Need to have a simple FastAPI that can upload files to S3.

## To Do (Engineering)
- Architect and implement a solution for uploading calls to S3 and then kicking off a mesasge to SQS.
- Add CloudFormation templates for S3 bucket and SQS queue.

## Readings
- Poetry
- ChromaDB
- Pydantic 
- LangGraph MemorySaver

## Poetry Commands
# Commands
```python
# Run fast api server in dev mode.
fastapi dev ./src/main.py
```

```python
poetry env activate
eval $(poetry env activate) 
```

```python
# Create a new poetry project.
poetry new <project_name>

# Deletes a poetry project.
poetry env remove <project_name>

# Adds a dependency.
poetry add <python_package>
```

```bash
# List environments.
ls ~/Library/Caches/pypoetry/virtualenvs/

# Location of environment.
~/Library/Caches/pypoetry/virtualenvs/backend-G3QjhxzE-py3.12/bin/activate
```