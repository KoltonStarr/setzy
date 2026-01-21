/**
 * Mock API service for local development
 * Simulates backend endpoints for audio file upload, transcription, and chat
 */

// Simulate network delay
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

// Mock storage for uploaded files
const mockFiles = new Map()
const mockTranscripts = new Map()

// Generate a mock transcript based on filename
const generateMockTranscript = (filename) => {
  const baseName = filename.replace(/\.[^/.]+$/, '')
  return `Transcript: ${baseName}

[00:00:00] Setter: Hi, this is Sarah calling from Smart Sellers Academy. Is this ${baseName}?

[00:00:05] Prospect: Yes, this is ${baseName}. How can I help you?

[00:00:08] Setter: Great! I'm calling to see if you might be interested in learning about our investment opportunities. Do you have a few minutes to talk?

[00:00:15] Prospect: Sure, I can spare a few minutes.

[00:00:18] Setter: Perfect! Just to set up the call for you really quick, the goal is just to get to know you a little better and for you to get to know us. If it's a good fit, typically we schedule another deeper call with our account executive. This is just more so a brief overview of our business, of what we do. Does that sound good?

[00:00:35] Prospect: That sounds reasonable. What kind of investment are we talking about?

[00:00:40] Setter: Well, we help people invest in e-commerce businesses. We manage active stores and provide a turnkey solution. What are your goals when it comes to investing?

[00:00:50] Prospect: I'm looking to diversify my portfolio and generate some passive income.

[00:00:55] Setter: That's great! How much are you looking to invest?

[00:01:00] Prospect: I'm thinking around $50,000 to start.

[00:01:05] Setter: Excellent! And what's your credit score like?

[00:01:10] Prospect: It's around 750.

[00:01:12] Setter: Perfect! That's a great score. Let me tell you a bit more about what we offer...

[Transcript continues...]`
}

/**
 * Upload audio file
 * @param {File} file - Audio file to upload
 * @returns {Promise<{fileId: string, status: string, message: string}>}
 */
export const uploadAudioFile = async (file) => {
  await delay(1000) // Simulate upload time

  const fileId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  
  mockFiles.set(fileId, {
    id: fileId,
    name: file.name,
    size: file.size,
    type: file.type,
    uploadedAt: new Date().toISOString(),
    status: 'uploaded',
  })

  return {
    fileId,
    status: 'uploaded',
    message: 'File uploaded successfully',
  }
}

/**
 * Start transcription for an uploaded file
 * @param {string} fileId - ID of the uploaded file
 * @returns {Promise<{status: string, transcriptId?: string}>}
 */
export const startTranscription = async (fileId) => {
  await delay(500) // Simulate API call

  const file = mockFiles.get(fileId)
  if (!file) {
    throw new Error('File not found')
  }

  // Update status to transcribing
  mockFiles.set(fileId, {
    ...file,
    status: 'transcribing',
  })

  return {
    status: 'transcribing',
    message: 'Transcription started',
  }
}

/**
 * Get transcription status
 * @param {string} fileId - ID of the file
 * @returns {Promise<{status: string, transcript?: string, progress?: number}>}
 */
export const getTranscriptionStatus = async (fileId) => {
  await delay(300) // Simulate API call

  const file = mockFiles.get(fileId)
  if (!file) {
    throw new Error('File not found')
  }

  // Simulate transcription progress
  if (file.status === 'transcribing') {
    // After 3 seconds, mark as completed
    const uploadTime = new Date(file.uploadedAt).getTime()
    const now = Date.now()
    const elapsed = now - uploadTime

    if (elapsed > 3000) {
      const transcript = generateMockTranscript(file.name)
      mockTranscripts.set(fileId, transcript)
      
      mockFiles.set(fileId, {
        ...file,
        status: 'completed',
        transcript,
      })

      return {
        status: 'completed',
        transcript,
        progress: 100,
      }
    } else {
      const progress = Math.min(90, Math.floor((elapsed / 3000) * 100))
      return {
        status: 'transcribing',
        progress,
      }
    }
  }

  if (file.status === 'completed') {
    return {
      status: 'completed',
      transcript: mockTranscripts.get(fileId) || file.transcript,
      progress: 100,
    }
  }

  return {
    status: file.status,
  }
}

/**
 * Get list of all uploaded files
 * @returns {Promise<Array<{id: string, name: string, status: string, uploadedAt: string}>>}
 */
export const listAudioFiles = async () => {
  await delay(300) // Simulate API call

  return Array.from(mockFiles.values()).map((file) => ({
    id: file.id,
    name: file.name,
    status: file.status,
    uploadedAt: file.uploadedAt,
    size: file.size,
  }))
}

/**
 * Get a single audio file
 * @param {string} fileId - ID of the file
 * @returns {Promise<{id: string, name: string, status: string, transcript?: string}>}
 */
export const getAudioFile = async (fileId) => {
  await delay(200) // Simulate API call

  const file = mockFiles.get(fileId)
  if (!file) {
    throw new Error('File not found')
  }

  return {
    id: file.id,
    name: file.name,
    status: file.status,
    transcript: mockTranscripts.get(fileId) || file.transcript,
    uploadedAt: file.uploadedAt,
  }
}

/**
 * Send a chat message about a transcript
 * @param {string} fileId - ID of the file/transcript
 * @param {string} message - User's message
 * @returns {Promise<{messageId: string, response: string}>}
 */
export const sendChatMessage = async (fileId, message) => {
  await delay(800 + Math.random() * 1200) // Simulate AI processing time (0.8-2s)

  const file = mockFiles.get(fileId)
  const transcript = mockTranscripts.get(fileId) || file?.transcript

  // Generate a mock response based on the message
  const responses = [
    `Based on the transcript, I can see that ${message.toLowerCase()}. Let me analyze the call data for you.`,
    `That's a great question! Looking at the transcript, I notice several relevant points that address your question about "${message}".`,
    `From analyzing this call, I can provide insights about "${message}". The transcript shows relevant information in the discovery phase.`,
    `I've reviewed the transcript and found information related to "${message}". Would you like me to dive deeper into any specific aspect?`,
  ]

  const response = responses[Math.floor(Math.random() * responses.length)]

  return {
    messageId: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    response,
    timestamp: new Date().toISOString(),
  }
}

/**
 * Poll transcription status until complete
 * @param {string} fileId - ID of the file
 * @param {Function} onProgress - Callback for progress updates
 * @returns {Promise<{status: string, transcript: string}>}
 */
export const waitForTranscription = async (fileId, onProgress) => {
  return new Promise((resolve, reject) => {
    const checkStatus = async () => {
      try {
        const status = await getTranscriptionStatus(fileId)
        
        if (onProgress) {
          onProgress(status)
        }

        if (status.status === 'completed') {
          resolve(status)
        } else if (status.status === 'error') {
          reject(new Error('Transcription failed'))
        } else {
          // Check again in 500ms
          setTimeout(checkStatus, 500)
        }
      } catch (error) {
        reject(error)
      }
    }

    checkStatus()
  })
}

// Mock thread storage for agent chat
const mockThreads = new Map()

/**
 * Send a chat message to the agent API
 * @param {string} message - User's message
 * @param {string|null} threadId - Optional thread ID for conversation continuity
 * @returns {Promise<{thread_id: string, message: string}>}
 */
export const sendChatMessageToAgent = async (message, threadId = null) => {
  await delay(800 + Math.random() * 1200) // Simulate AI processing time (0.8-2s)

  // Generate or use thread ID
  const currentThreadId = threadId || `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`
  
  // Get or create thread messages
  if (!mockThreads.has(currentThreadId)) {
    mockThreads.set(currentThreadId, [])
  }
  const threadMessages = mockThreads.get(currentThreadId)
  threadMessages.push({ role: 'user', content: message })

  // Generate a mock response
  const responses = [
    `I understand you're asking about "${message}". Let me help you with that.`,
    `That's an interesting question! Regarding "${message}", I can provide some insights.`,
    `Thanks for your question about "${message}". Here's what I think...`,
    `I see you're interested in "${message}". Let me share some relevant information.`,
  ]

  const response = responses[Math.floor(Math.random() * responses.length)]
  threadMessages.push({ role: 'assistant', content: response })

  return {
    thread_id: currentThreadId,
    message: response,
  }
}
