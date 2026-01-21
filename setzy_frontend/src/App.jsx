import { useState, useCallback, useEffect } from 'react'
import FileDropzone from './components/FileDropzone'
import ChatColumn from './components/ChatColumn'
import * as api from './services/api'
import './App.css'

function App() {
  const [files, setFiles] = useState([])
  const [generalChat, setGeneralChat] = useState({
    messages: [],
    threadId: null,
    isMinimized: false,
  })

  const handleFilesAccepted = useCallback(async (acceptedFiles) => {
    // Process only the first file (single file upload)
    const file = acceptedFiles[0]
    if (!file) return

    try {
      // Upload file to uploader service
      const uploadResult = await api.uploadAudioFile(file)
      const fileId = uploadResult.fileId

      // Create initial file entry
      const newFile = {
        id: fileId,
        file: file,
        name: file.name,
        status: 'completed', // File is uploaded, ready for chat
        transcript: null,
        messages: [],
        isMinimized: false,
        createdAt: new Date().toISOString(),
      }

      // Add file to state
      setFiles((prev) => [newFile, ...prev])
    } catch (error) {
      console.error('Error uploading file:', file.name, error)
      // Could show error notification here
    }
  }, [])

  const handleToggleMinimize = useCallback((fileId) => {
    setFiles((prev) =>
      prev.map((f) =>
        f.id === fileId ? { ...f, isMinimized: !f.isMinimized } : f
      )
    )
  }, [])

  const handleAddMessage = useCallback(async (fileId, message) => {
    // Add user message immediately
    const userMessage = {
      id: `${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    }

    setFiles((prev) =>
      prev.map((f) =>
        f.id === fileId
          ? {
              ...f,
              messages: [...f.messages, userMessage],
            }
          : f
      )
    )

    // Get AI response (using agent API)
    try {
      const response = await api.sendChatMessageToAgent(message, null)
      
      const assistantMessage = {
        id: `${Date.now()}`,
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
      }

      setFiles((prev) =>
        prev.map((f) =>
          f.id === fileId
            ? {
                ...f,
                messages: [...f.messages, assistantMessage],
              }
            : f
        )
      )
    } catch (error) {
      console.error('Error sending message:', error)
      // Add error message
      const errorMessage = {
        id: `${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      }
      setFiles((prev) =>
        prev.map((f) =>
          f.id === fileId
            ? {
                ...f,
                messages: [...f.messages, errorMessage],
              }
            : f
        )
      )
    }
  }, [])

  const handleGeneralChatMessage = useCallback(async (message) => {
    // Add user message immediately
    const userMessage = {
      id: `${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    }

    setGeneralChat((prev) => ({
      ...prev,
      messages: [...prev.messages, userMessage],
    }))

    // Get AI response from agent API
    try {
      const response = await api.sendChatMessageToAgent(message, generalChat.threadId)
      
      const assistantMessage = {
        id: `${Date.now()}`,
        role: 'assistant',
        content: response.message,
        timestamp: new Date().toISOString(),
      }

      setGeneralChat((prev) => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        threadId: response.thread_id, // Update thread ID for continuity
      }))
    } catch (error) {
      console.error('Error sending message to agent:', error)
      // Add error message
      const errorMessage = {
        id: `${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      }
      setGeneralChat((prev) => ({
        ...prev,
        messages: [...prev.messages, errorMessage],
      }))
    }
  }, [generalChat.threadId])

  const handleToggleGeneralChatMinimize = useCallback(() => {
    setGeneralChat((prev) => ({
      ...prev,
      isMinimized: !prev.isMinimized,
    }))
  }, [])

  const handleExport = useCallback((fileId, format) => {
    const fileObj = files.find((f) => f.id === fileId)
    if (!fileObj) return

    let content = ''
    let mimeType = ''
    let extension = ''

    switch (format) {
      case 'txt':
        content = fileObj.transcript || 'No transcript available'
        mimeType = 'text/plain'
        extension = 'txt'
        break
      case 'json':
        content = JSON.stringify(
          {
            filename: fileObj.name,
            transcript: fileObj.transcript,
            messages: fileObj.messages,
            createdAt: fileObj.createdAt,
          },
          null,
          2
        )
        mimeType = 'application/json'
        extension = 'json'
        break
      case 'csv':
        const csvRows = [
          ['Role', 'Content', 'Timestamp'],
          ...fileObj.messages.map((msg) => [
            msg.role,
            `"${msg.content.replace(/"/g, '""')}"`,
            msg.timestamp,
          ]),
        ]
        content = csvRows.map((row) => row.join(',')).join('\n')
        mimeType = 'text/csv'
        extension = 'csv'
        break
      case 'md':
        content = `# ${fileObj.name}\n\n## Transcript\n\n${fileObj.transcript || 'No transcript available'}\n\n## Chat History\n\n${fileObj.messages.map((msg) => `### ${msg.role}\n\n${msg.content}\n`).join('\n')}`
        mimeType = 'text/markdown'
        extension = 'md'
        break
      default:
        return
    }

    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${fileObj.name.replace(/\.[^/.]+$/, '')}.${extension}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }, [files])

  return (
    <div className="app">
      <header className="app-header">
        <h1>Setzy</h1>
        <p className="app-subtitle">Sales Call Manager</p>
      </header>
      <main className="app-main">
        <div className="app-layout">
          <aside className="app-sidebar">
            <FileDropzone
              onFilesAccepted={handleFilesAccepted}
              files={files}
            />
          </aside>
          <section className="app-chats">
            {/* General Chat - always show */}
            <ChatColumn
              key="general-chat"
              isGeneralChat={true}
              messages={generalChat.messages}
              isMinimized={generalChat.isMinimized}
              onToggleMinimize={handleToggleGeneralChatMinimize}
              onAddMessage={handleGeneralChatMessage}
            />
            {/* File-specific chats */}
            {files.map((fileObj) => (
              <ChatColumn
                key={fileObj.id}
                file={fileObj}
                messages={fileObj.messages}
                isMinimized={fileObj.isMinimized}
                onToggleMinimize={() => handleToggleMinimize(fileObj.id)}
                onAddMessage={(message) =>
                  handleAddMessage(fileObj.id, message)
                }
                onExport={(format) => handleExport(fileObj.id, format)}
              />
            ))}
            {files.length === 0 && generalChat.messages.length === 0 && (
              <div className="empty-state">
                <p>Upload an audio file or start chatting</p>
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  )
}

export default App

