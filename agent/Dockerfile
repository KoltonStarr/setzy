# Build stage - Install dependencies
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY agent/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage - Runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies (including shell utilities)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files from agent directory
COPY agent/main.py agent/tools.py agent/system_prompt.py ./

# Copy .env file from project root
COPY .env .env

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command - run the agent
CMD ["python", "main.py"]
