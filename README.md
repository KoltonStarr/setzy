## To Do (Agent)
- Make the system prompt structured:
--- I could put it at the root of the project in 2 flavors. One prompt that is shared between the two and then the 
other would just be for the agent. 
--- Make one unified system prompt that both the data pipeline and the agent use. 
--- Need to enforce some sort of schema (maybe for now just make it a suggestion.)

## To Do (Data Pipeline)
- DONE

## To Do (Backend)
- DONE

## To Do (Vector DB)
- DONE

## TO DO (Frontend)

## To Do (Engineering)
- Make sure the docker-compose works seamlessly. 
- Develop a thorough README of how to use the project.

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

## Readings
- Poetry
- ChromaDB
- Pydantic 
- LangGraph MemorySaver

## Backlog
- Add configuration to control the size of the agent's memory. Add code to clear message history when memory limit has been reached. 
- Protect the endpoint with oauth / STS connection.