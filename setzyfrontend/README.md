# Setzy Frontend

A modern React-based frontend for the Setzy Sales Call Manager application.

## Features

- **Dark Mode**: Automatically enabled dark theme
- **File Upload**: Drag-and-drop interface for multiple audio file types
- **Real-time Transcription**: Chat columns appear as files are transcribed
- **Minimizable Chats**: Click to expand/collapse individual chat sessions
- **Export Functionality**: Export transcripts and chat history in multiple formats (TXT, JSON, CSV, Markdown)

## Tech Stack

- React 18
- Vite (build tool)
- react-dropzone (file uploads)
- Nginx (production server)

## Development

### Prerequisites

- Node.js 20+ and npm

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

### Build

```bash
# Build for production
npm run build
```

The built files will be in the `dist/` directory.

## Docker

### Build Docker Image

```bash
docker build -t setzy-frontend .
```

### Run Docker Container

```bash
docker run -p 8080:80 setzy-frontend
```

The app will be available at `http://localhost:8080`

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── FileDropzone.jsx # File upload component
│   │   ├── ChatColumn.jsx   # Individual chat column
│   │   ├── ChatHeader.jsx   # Chat header with minimize/export
│   │   ├── ChatMessages.jsx # Message display
│   │   └── ChatInput.jsx    # Message input
│   ├── services/            # API services
│   │   ├── api.js           # Main API service (switches between mock/real)
│   │   └── mockApi.js        # Mock API implementation
│   ├── App.jsx              # Main application component
│   ├── App.css              # App styles
│   ├── main.jsx             # React entry point
│   └── index.css            # Global styles
├── index.html               # HTML template
├── vite.config.js           # Vite configuration
├── package.json             # Dependencies
├── Dockerfile               # Multi-stage Docker build
└── nginx.conf               # Nginx configuration
```

## Supported Audio Formats

- MP3, WAV, M4A, OGG, WebM, AAC, FLAC
- MP4, MOV (video files with audio)

## Mock API

The frontend includes a complete mock API system for local development. The mocks simulate:

- **File Upload**: Simulates uploading audio files to S3
- **Transcription**: Simulates the transcription process with realistic delays
- **Chat Messages**: Generates contextual AI responses based on user queries
- **File Management**: Tracks file status and metadata

### Using Mock API

By default, the app uses mock APIs. To switch to a real backend API:

1. Create a `.env` file in the frontend directory:
```bash
VITE_USE_MOCK_API=false
VITE_API_BASE_URL=http://localhost:8000/api
```

2. Or set environment variables when running:
```bash
VITE_USE_MOCK_API=false npm run dev
```

### Mock API Features

- **Realistic Delays**: Simulates network latency and processing time
- **Progress Updates**: Shows transcription progress in real-time
- **Contextual Responses**: Mock chat responses vary based on user input
- **File Persistence**: Mock files are stored in memory during the session

## Notes

- Mock API is enabled by default for easy local development
- Backend API integration is ready - just set `VITE_USE_MOCK_API=false`
- Google OIDC authentication can be added as per requirements

