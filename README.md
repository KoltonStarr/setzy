# Setzy

Self-hosted AI tooling for call data: upload audio, generate transcripts and embeddings, and chat with an agent grounded in your data. This repo provides Dockerized services for a vector database (ChromaDB), an uploader API, an embedding pipeline, and a chat agent.

## Table of Contents
- Overview
- Architecture
- Prerequisites
- Environment Setup
- Create S3 Bucket
- Build Images
- Run Locally
- Test the APIs
- Troubleshooting
- Frontend

## Overview
Setzy is a self-hosted open source project. It enables:
- Uploading audio files to S3
- Diarizing and transcribing audio (AssemblyAI)
- Chunking transcripts into documents and embedding to ChromaDB
- Chatting with an agent that answers questions using the vector store

## Architecture
- ChromaDB (chromadb): Vector DB exposed on port 8000, configured with OpenTelemetry and Zipkin.
- Agent (setzy_agent): FastAPI service on port 8081 that streams responses from an LLM and calls tools (vector search, web search).
- Uploader (setzy_uploader): FastAPI service on port 8080 to upload audio files directly to S3.
- Pipeline (setzy_pipeline): Batch job that pulls audio from S3, diarizes, transcribes, creates documents, and writes embeddings to Chroma. Disabled by default via Compose profile.
- Observability: otel-collector and zipkin (Zipkin on 9411).

## Prerequisites
Run the dependency checker to verify your environment:

```bash
./check_dependencies.sh
```

Required tools (macOS):
- Docker Desktop (includes Docker & Docker Compose)
- Python 3.12.12+
- Poetry
- AWS CLI (with credentials configured)
- Node.js + npm (for frontend, when ready)
- Git

If any checks fail, follow the links printed by `check_dependencies.sh` and re-run it.

## Environment Setup
Create a `.env` file at the repo root. Minimal variables:

```dotenv
# OpenAI key for the agent (LangChain OpenAI integration)
OPENAI_API_KEY=your-openai-key

# AssemblyAI for transcription
ASSEMBLYAI_API_KEY=your-assemblyai-key

# S3 bucket for audio storage
S3_BUCKET_NAME=your-s3-bucket

# Optional: ChromaDB host (Compose sets this to 'chromadb' in containers)
CHROMADB_HOST=chromadb
```

Notes:
- The agent uses LangChain with an OpenAI model and expects `OPENAI_API_KEY`.
- The pipeline uses `ASSEMBLYAI_API_KEY` and `S3_BUCKET_NAME`.
- Docker Compose mounts `~/.aws` into uploader/pipeline containers to use your AWS CLI credentials.

## Create S3 Bucket
Use CloudFormation to create the bucket, then copy the name into `.env`:

```bash
./create_bucket.sh
```

The script prints `S3_BUCKET_NAME=...`. Add that line to your `.env`.

Alternatively, create a bucket manually with the AWS Console or CLI and set `S3_BUCKET_NAME` accordingly.

## Build Images
You can build services individually. A helper script is provided:

```bash
# Agent service
./build_images.sh agent

# Embedding pipeline service
./build_images.sh pipeline

# Uploader service
./build_images.sh uploader

# Frontend (not yet implemented in the script)
./build_images.sh frontend  # will print not implemented
```

Or build via Docker Compose (builds on first `up`):

```bash
docker compose build
```

## Run Locally
Start the default stack (ChromaDB, Agent, Uploader, Zipkin, Otel Collector):

```bash
docker compose up -d
```

This brings up:
- ChromaDB on http://localhost:8000
- Agent on http://localhost:8081
- Uploader on http://localhost:8080
- Zipkin on http://localhost:9411

Start the embedding pipeline when ready (disabled by default via profile):

```bash
docker compose --profile pipeline up -d pipeline
```

Check containers:

```bash
docker ps
```

Stop everything:

```bash
docker compose down
```

## Test the APIs

### Uploader (port 8080)
Upload an audio file to S3:

```bash
curl -X POST \
  -F "file=@setzy_uploader/tests/audio_upload/Debra Ajayi.wav" \
  http://localhost:8080/upload
```

Return value: `{ "message": "success }` on success.

You can also run the provided test scripts:

```bash
./setzy_uploader/tests/audio_upload/run.sh
./setzy_uploader/tests/textfile_upload/run.sh
```

### Agent (port 8081)
Start a new chat:

```bash
curl -X POST http://localhost:8081/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Setzy?",
    "thread_id": null
  }'
```

Send a follow-up using the returned `thread_id`:

```bash
curl -X POST http://localhost:8081/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me more",
    "thread_id": "<paste-thread-id>"
  }'
```

### ChromaDB (port 8000)
ChromaDB is exposed on port 8000. The pipeline writes embeddings; the agent queries them via tools.

## Troubleshooting
- Ensure Docker Desktop is running and `docker ps` shows containers.
- Verify `.env` variables are present: `OPENAI_API_KEY`, `ASSEMBLYAI_API_KEY`, `S3_BUCKET_NAME`.
- Check AWS credentials: run `aws sts get-caller-identity`; ensure `~/.aws` exists for container mounts.
- Logs:
  - Agent: `docker logs setzy-agent`
  - Uploader: `docker logs setzy-uploader`
  - Pipeline: `docker logs setzy-pipeline`
  - ChromaDB: `docker logs chromadb`
- Zipkin UI: http://localhost:9411

If Compose build fails due to path mismatches, confirm Dockerfile locations under `setzy_agent/`, `setzy_pipeline`, and `setzy_uploader` and update `docker-compose.yml` accordingly.

## Frontend

