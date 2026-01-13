# Connecting Frontend to Backend

This guide explains how to connect the React frontend to the backend API.

## Current Setup

The frontend is configured to automatically switch between mock and real APIs based on environment variables. By default, it uses mocks for local development.

## Connecting to Backend

### Step 1: Create Environment File

Create a `.env` file in the `setzy/frontend/` directory:

```bash
# Disable mock API
VITE_USE_MOCK_API=false

# Set your backend API URL
VITE_API_BASE_URL=http://localhost:8000/api
```

**For Docker/Production:**
```bash
VITE_USE_MOCK_API=false
VITE_API_BASE_URL=http://backend:8000/api
```

### Step 2: Backend API Requirements

Your backend must implement these endpoints:

#### 1. Upload Audio File
```
POST /api/audio/upload
Content-Type: multipart/form-data
Body: file (audio file)

Response:
{
  "fileId": "string",
  "status": "uploaded",
  "message": "File uploaded successfully"
}
```

#### 2. Start Transcription
```
POST /api/audio/{fileId}/transcribe

Response:
{
  "status": "transcribing",
  "message": "Transcription started"
}
```

#### 3. Get Transcription Status
```
GET /api/audio/{fileId}/status

Response (processing):
{
  "status": "transcribing",
  "progress": 45
}

Response (completed):
{
  "status": "completed",
  "transcript": "Full transcript text...",
  "progress": 100
}
```

#### 4. List Audio Files
```
GET /api/audio

Response:
[
  {
    "id": "string",
    "name": "string",
    "status": "completed",
    "uploadedAt": "ISO8601 timestamp",
    "size": 12345
  }
]
```

#### 5. Get Single Audio File
```
GET /api/audio/{fileId}

Response:
{
  "id": "string",
  "name": "string",
  "status": "completed",
  "transcript": "Full transcript text...",
  "uploadedAt": "ISO8601 timestamp"
}
```

#### 6. Send Chat Message
```
POST /api/chat/{fileId}/message
Content-Type: application/json
Body: { "message": "user's question" }

Response:
{
  "messageId": "string",
  "response": "AI response text",
  "timestamp": "ISO8601 timestamp"
}
```

### Step 3: CORS Configuration

Ensure your backend allows CORS requests from the frontend:

**Python (Flask/FastAPI):**
```python
from flask_cors import CORS
CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])

# Or for FastAPI
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 4: Test Connection

1. Start your backend server
2. Update `.env` file with backend URL
3. Restart the frontend dev server:
   ```bash
   npm run dev
   ```
4. Try uploading a file - it should connect to your backend

## Development vs Production

### Development (Local)
```bash
# Frontend runs on http://localhost:5173 (Vite default)
# Backend should run on http://localhost:8000
VITE_API_BASE_URL=http://localhost:8000/api
```

### Production (Docker)
```bash
# Use service names in docker-compose
VITE_API_BASE_URL=http://backend:8000/api
```

## Troubleshooting

### CORS Errors
- Ensure backend CORS is configured correctly
- Check that the backend URL in `.env` matches your backend server

### Connection Refused
- Verify backend is running
- Check the `VITE_API_BASE_URL` is correct
- For Docker, ensure services are on the same network

### Still Using Mocks
- Verify `.env` file exists in `frontend/` directory
- Ensure `VITE_USE_MOCK_API=false` (not `"false"` as a string)
- Restart the dev server after changing `.env`

## API Service Architecture

The frontend uses a service layer (`src/services/api.js`) that:
- Automatically switches between mock and real API
- Handles all HTTP requests
- Provides consistent error handling
- No component changes needed when switching APIs

