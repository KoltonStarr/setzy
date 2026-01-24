## To Do (CLI Client)
- Develop a simple CLI client as an alternative to the frontend.
- It should be able to send files to the uploader
- It should be able to talk with the agent in a loop and use the API. 

## To Do (Engineering)
- Publish the images and reference them in the docker-compose.
- Figure out licensing for open source. 
- Figure out SEO.

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