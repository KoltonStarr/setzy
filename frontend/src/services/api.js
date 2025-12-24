/**
 * API service for backend communication
 * Switch between mock and real API based on environment
 */

import * as mockApi from './mockApi'

// Determine if we should use mocks
const USE_MOCKS = import.meta.env.VITE_USE_MOCK_API !== 'false'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

/**
 * Upload audio file
 */
export const uploadAudioFile = async (file) => {
  if (USE_MOCKS) {
    return mockApi.uploadAudioFile(file)
  }

  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/audio/upload`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Upload failed')
  }

  return response.json()
}

/**
 * Start transcription
 */
export const startTranscription = async (fileId) => {
  if (USE_MOCKS) {
    return mockApi.startTranscription(fileId)
  }

  const response = await fetch(`${API_BASE_URL}/audio/${fileId}/transcribe`, {
    method: 'POST',
  })

  if (!response.ok) {
    throw new Error('Transcription start failed')
  }

  return response.json()
}

/**
 * Get transcription status
 */
export const getTranscriptionStatus = async (fileId) => {
  if (USE_MOCKS) {
    return mockApi.getTranscriptionStatus(fileId)
  }

  const response = await fetch(`${API_BASE_URL}/audio/${fileId}/status`)

  if (!response.ok) {
    throw new Error('Failed to get status')
  }

  return response.json()
}

/**
 * List all audio files
 */
export const listAudioFiles = async () => {
  if (USE_MOCKS) {
    return mockApi.listAudioFiles()
  }

  const response = await fetch(`${API_BASE_URL}/audio`)

  if (!response.ok) {
    throw new Error('Failed to list files')
  }

  return response.json()
}

/**
 * Get single audio file
 */
export const getAudioFile = async (fileId) => {
  if (USE_MOCKS) {
    return mockApi.getAudioFile(fileId)
  }

  const response = await fetch(`${API_BASE_URL}/audio/${fileId}`)

  if (!response.ok) {
    throw new Error('Failed to get file')
  }

  return response.json()
}

/**
 * Send chat message
 */
export const sendChatMessage = async (fileId, message) => {
  if (USE_MOCKS) {
    return mockApi.sendChatMessage(fileId, message)
  }

  const response = await fetch(`${API_BASE_URL}/chat/${fileId}/message`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  })

  if (!response.ok) {
    throw new Error('Failed to send message')
  }

  return response.json()
}

/**
 * Wait for transcription to complete
 */
export const waitForTranscription = async (fileId, onProgress) => {
  if (USE_MOCKS) {
    return mockApi.waitForTranscription(fileId, onProgress)
  }

  // Real implementation would poll the status endpoint
  return mockApi.waitForTranscription(fileId, onProgress)
}


