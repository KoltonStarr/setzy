# Quick Start Guide

## Connecting to Backend

### Option 1: Using Environment File (Recommended)

1. Create `.env` file in `setzy/frontend/`:
```bash
VITE_USE_MOCK_API=false
VITE_API_BASE_URL=http://localhost:8000/api
```

2. Restart dev server:
```bash
npm run dev
```

### Option 2: Using Docker with Backend

1. Update `docker-compose.yml` in project root
2. Build and run:
```bash
docker-compose up --build
```

## Using Docker

### Build Frontend Image

```bash
cd setzy/frontend
docker build -t setzy-frontend .
```

### Run Container

```bash
# With mocks (default)
docker run -p 8080:80 setzy-frontend

# With backend (pass build args)
docker build \
  --build-arg VITE_USE_MOCK_API=false \
  --build-arg VITE_API_BASE_URL=http://backend:8000/api \
  -t setzy-frontend .
```

### Using Docker Compose

```bash
# From project root
docker-compose up --build
```

Frontend: http://localhost:3000  
Backend: http://localhost:8000

## Development

```bash
# Install dependencies
npm install

# Run with mocks (default)
npm run dev

# Run with backend
# 1. Create .env file (see above)
# 2. npm run dev
```

## Important Notes

- **Environment variables must be set at BUILD TIME** for Docker
- Vite embeds env vars during `npm run build`
- For Docker, use `--build-arg` or update Dockerfile
- For local dev, use `.env` file

See `BACKEND_CONNECTION.md` and `DOCKER_GUIDE.md` for detailed instructions.

