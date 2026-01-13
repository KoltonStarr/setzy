# Docker Guide for Frontend

This guide explains how to build and run the frontend using Docker.

## Quick Start

### Build Docker Image

```bash
cd setzy/frontend
docker build -t setzy-frontend .
```

### Run Container

```bash
docker run -p 8080:80 setzy-frontend
```

The app will be available at `http://localhost:8080`

## Dockerfile Overview

The Dockerfile uses a **multi-stage build**:

1. **Builder Stage**: Uses Node.js to build the React app
2. **Production Stage**: Uses Nginx to serve static files

This results in a small, optimized production image (~50MB).

## Building with Environment Variables

### For Development (with mocks)

```bash
docker build -t setzy-frontend .
docker run -p 8080:80 setzy-frontend
```

### For Production (with backend)

Build with environment variables:

```bash
docker build \
  --build-arg VITE_USE_MOCK_API=false \
  --build-arg VITE_API_BASE_URL=http://backend:8000/api \
  -t setzy-frontend .
```

Or use a `.env` file during build (requires Docker BuildKit):

```bash
# .env.docker
VITE_USE_MOCK_API=false
VITE_API_BASE_URL=http://backend:8000/api

docker build --env-file .env.docker -t setzy-frontend .
```

**Note**: Vite requires environment variables at build time, not runtime. You must rebuild the image when changing API settings.

## Docker Compose Integration

### Example docker-compose.yml

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      args:
        - VITE_USE_MOCK_API=false
        - VITE_API_BASE_URL=http://backend:8000/api
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - setzy-network

  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    environment:
      - S3_BUCKET_NAME=your-bucket
      - AWS_ACCESS_KEY_ID=your-key
      - AWS_SECRET_ACCESS_KEY=your-secret
    networks:
      - setzy-network

networks:
  setzy-network:
    driver: bridge
```

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f frontend

# Stop services
docker-compose down
```

## Updating Dockerfile for Build Args

If you want to pass environment variables at build time, update the Dockerfile:

```dockerfile
# Multi-stage build for React frontend
FROM node:20-alpine AS builder

WORKDIR /app

# Accept build arguments
ARG VITE_USE_MOCK_API=true
ARG VITE_API_BASE_URL=http://localhost:8000/api

# Set as environment variables for Vite
ENV VITE_USE_MOCK_API=$VITE_USE_MOCK_API
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Copy package files
COPY package.json ./
COPY package-lock.json* ./

# Install dependencies
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

## Production Considerations

### 1. Environment Variables

Vite embeds environment variables at build time. For different environments:

- **Development**: Build with mocks enabled
- **Staging**: Build with staging backend URL
- **Production**: Build with production backend URL

### 2. Nginx Configuration

The `nginx.conf` is already configured for:
- SPA routing (all routes serve index.html)
- Gzip compression
- Security headers
- Large file uploads (100MB limit)

### 3. Health Checks

Add to docker-compose.yml:

```yaml
services:
  frontend:
    # ... other config
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Troubleshooting

### Build Fails

```bash
# Clear Docker cache
docker builder prune

# Build without cache
docker build --no-cache -t setzy-frontend .
```

### Port Already in Use

```bash
# Use different port
docker run -p 3000:80 setzy-frontend
```

### Environment Variables Not Working

Remember: Vite requires env vars at **build time**, not runtime. Rebuild the image after changing environment variables.

### Nginx 404 Errors

Ensure `nginx.conf` has the SPA routing rule:
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

## Image Size Optimization

The current setup produces a ~50MB image. To optimize further:

1. Use `.dockerignore` (already included)
2. Multi-stage build (already implemented)
3. Alpine Linux base images (already using nginx:alpine)

## Next Steps

1. Integrate with your backend API
2. Set up CI/CD pipeline
3. Configure production environment variables
4. Set up monitoring and logging

