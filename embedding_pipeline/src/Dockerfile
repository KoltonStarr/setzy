# Build stage - Install dependencies
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies and Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Configure Poetry to not create virtual environment in Docker
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Copy poetry files
COPY embedding_pipeline/pyproject.toml embedding_pipeline/poetry.lock* ./

# Install dependencies
RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR

# Final stage - Runtime
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application files
COPY embedding_pipeline/src ./src
COPY .env ./

# Create data and transcripts directories
RUN mkdir -p /app/data /app/transcripts

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    DATA_DIR=/app/data \
    TRANSCRIPTS_DIR=/app/transcripts

# Default command - run the embedding pipeline
CMD ["python", "src/main.py"]
