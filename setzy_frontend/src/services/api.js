/**
 * API service for backend communication
 * Switch between mock and real API based on environment
 */

import * as mockApi from './mockApi'

// Determine if we should use mocks
const USE_MOCKS = import.meta.env.VITE_USE_MOCK_API !== 'false'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
const UPLOADER_BASE_URL = import.meta.env.VITE_UPLOADER_BASE_URL || 'http://localhost:8080'
const AGENT_BASE_URL = import.meta.env.VITE_AGENT_BASE_URL || 'http://localhost:8081'

/**
 * Generate a unique file ID
 */
const generateFileId = (filename) => {
  const timestamp = Date.now()
  const random = Math.random().toString(36).substring(2, 9)
  return `${timestamp}-${random}-${filename}`
}

/**
 * Upload audio file
 */
export const uploadAudioFile = async (file) => {
  if (USE_MOCKS) {
    return mockApi.uploadAudioFile(file)
  }

  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${UPLOADER_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Upload failed')
  }

  const result = await response.json()
  
  // Generate fileId on frontend since backend doesn't return one
  const fileId = generateFileId(file.name)
  
  return {
    fileId,
    status: 'uploaded',
    message: result.message || 'File uploaded successfully',
  }
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

/**
 * Send chat message to agent API
 * @param {string} message - User's message
 * @param {string|null} threadId - Optional thread ID for conversation continuity
 * @returns {Promise<{thread_id: string, message: string}>}
 */
export const sendChatMessageToAgent = async (message, threadId = null) => {
  if (USE_MOCKS) {
    return mockApi.sendChatMessageToAgent(message, threadId)
  }

  const response = await fetch(`${AGENT_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      thread_id: threadId,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to send message to agent')
  }

  return response.json()
}


