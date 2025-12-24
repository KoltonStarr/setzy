# Mock API Documentation

This document describes the mock API system used for local development.

## Overview

The mock API system provides a complete simulation of the backend API, allowing you to develop and test the frontend without a running backend server. All mock functions simulate realistic network delays and return appropriate data structures.

## Usage

### Default Behavior

By default, the app uses mock APIs. No configuration is needed - just run:

```bash
npm install
npm run dev
```

### Switching to Real API

To use a real backend API, create a `.env` file:

```bash
VITE_USE_MOCK_API=false
VITE_API_BASE_URL=http://localhost:8000/api
```

## Mock API Endpoints

### `uploadAudioFile(file: File)`

Uploads an audio file and returns a file ID.

**Response:**
```json
{
  "fileId": "1234567890-abc123",
  "status": "uploaded",
  "message": "File uploaded successfully"
}
```

**Simulated Delay:** ~1 second

---

### `startTranscription(fileId: string)`

Starts the transcription process for an uploaded file.

**Response:**
```json
{
  "status": "transcribing",
  "message": "Transcription started"
}
```

**Simulated Delay:** ~500ms

---

### `getTranscriptionStatus(fileId: string)`

Gets the current status of a transcription.

**Response (while transcribing):**
```json
{
  "status": "transcribing",
  "progress": 45
}
```

**Response (when complete):**
```json
{
  "status": "completed",
  "transcript": "Full transcript text...",
  "progress": 100
}
```

**Simulated Delay:** ~300ms

---

### `waitForTranscription(fileId: string, onProgress: Function)`

Polls the transcription status until completion, calling `onProgress` with status updates.

**Returns:** Promise that resolves when transcription is complete

**Total Simulated Time:** ~3-4 seconds

---

### `sendChatMessage(fileId: string, message: string)`

Sends a chat message about a transcript and gets an AI response.

**Response:**
```json
{
  "messageId": "1234567890-xyz789",
  "response": "Based on the transcript, I can see that...",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Simulated Delay:** 0.8-2 seconds (randomized)

---

### `listAudioFiles()`

Returns a list of all uploaded audio files.

**Response:**
```json
[
  {
    "id": "1234567890-abc123",
    "name": "call-recording.mp3",
    "status": "completed",
    "uploadedAt": "2024-01-01T12:00:00.000Z",
    "size": 5242880
  }
]
```

---

### `getAudioFile(fileId: string)`

Gets details about a specific audio file.

**Response:**
```json
{
  "id": "1234567890-abc123",
  "name": "call-recording.mp3",
  "status": "completed",
  "transcript": "Full transcript text...",
  "uploadedAt": "2024-01-01T12:00:00.000Z"
}
```

## Mock Transcript Generation

The mock API generates realistic transcripts based on the filename. Each transcript includes:

- Timestamped speaker segments
- Realistic conversation flow
- Multiple call phases (Introduction, Discovery, etc.)
- Varied content based on filename

## Implementation Details

### Storage

- Mock files are stored in memory using JavaScript `Map` objects
- Data persists only during the current browser session
- No data is persisted to disk or external storage

### Timing

All API calls include simulated network delays:
- Upload: ~1 second
- Transcription start: ~500ms
- Status checks: ~300ms
- Transcription completion: ~3-4 seconds total
- Chat responses: 0.8-2 seconds (randomized)

### Error Handling

The mock API includes basic error handling:
- Returns appropriate error messages for missing files
- Simulates network errors occasionally (can be extended)

## Customization

To customize mock behavior, edit `src/services/mockApi.js`:

- Adjust delays by modifying the `delay()` function calls
- Modify transcript generation in `generateMockTranscript()`
- Change chat responses in `sendChatMessage()`
- Add more realistic error scenarios

## Testing

The mock API is designed to be:
- **Deterministic**: Same inputs produce consistent outputs
- **Realistic**: Simulates real-world timing and behavior
- **Flexible**: Easy to extend with new features

## Migration to Real API

When switching to a real backend:

1. Set `VITE_USE_MOCK_API=false` in `.env`
2. Set `VITE_API_BASE_URL` to your backend URL
3. Ensure your backend implements the same API contract
4. The `api.js` service will automatically use real endpoints

No code changes are needed in components - they all use the `api.js` service which handles the switch automatically.


