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
- Add real persistence for the agent's memory.  
- Protect the endpoint with oauth / STS connection.
- Add query expansion / transformation logic so that the query is embedded better to improve results.
- Containerize the CLI client. 