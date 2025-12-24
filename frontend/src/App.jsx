import { useState, useCallback, useEffect } from 'react'
import FileDropzone from './components/FileDropzone'
import ChatColumn from './components/ChatColumn'
import * as api from './services/api'
import './App.css'

function App() {
  const [files, setFiles] = useState([])

  const handleFilesAccepted = useCallback(async (acceptedFiles) => {
    // Process each file
    for (const file of acceptedFiles) {
      try {
        // Upload file first to get fileId from API
        const uploadResult = await api.uploadAudioFile(file)
        const fileId = uploadResult.fileId

        // Create initial file entry
        const newFile = {
          id: fileId,
          file: file,
          name: file.name,
          status: 'uploading',
          transcript: null,
          messages: [],
          isMinimized: false,
          createdAt: new Date().toISOString(),
        }

        // Add file to state
        setFiles((prev) => [newFile, ...prev])
        
        // Update status to transcribing
        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileId ? { ...f, status: 'transcribing' } : f
          )
        )

        // Start transcription
        await api.startTranscription(fileId)

        // Wait for transcription to complete with progress updates
        await api.waitForTranscription(fileId, (status) => {
          setFiles((prev) =>
            prev.map((f) =>
              f.id === fileId
                ? {
                    ...f,
                    status: status.status,
                    transcript: status.transcript || f.transcript,
                  }
                : f
            )
          )
        })

        // Transcription complete - move to top and minimize
        setFiles((prev) => {
          const updated = prev.map((f) =>
            f.id === fileId
              ? {
                  ...f,
                  status: 'completed',
                  isMinimized: true,
                }
              : f
          )
          // Move completed file to the top
          const completedFile = updated.find((f) => f.id === fileId)
          if (completedFile) {
            const withoutCompleted = updated.filter((f) => f.id !== fileId)
            return [completedFile, ...withoutCompleted]
          }
          return updated
        })
      } catch (error) {
        console.error('Error processing file:', file.name, error)
        // Find and update the file that failed
        setFiles((prev) =>
          prev.map((f) =>
            f.name === file.name && f.status === 'uploading'
              ? { ...f, status: 'error' }
              : f
          )
        )
      }
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

    // Get AI response
    try {
      const response = await api.sendChatMessage(fileId, message)
      
      const assistantMessage = {
        id: response.messageId,
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
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
            {files.length === 0 ? (
              <div className="empty-state">
                <p>Upload audio files to start transcribing</p>
              </div>
            ) : (
              files.map((fileObj) => (
                <ChatColumn
                  key={fileObj.id}
                  file={fileObj}
                  onToggleMinimize={() => handleToggleMinimize(fileObj.id)}
                  onAddMessage={(message) =>
                    handleAddMessage(fileObj.id, message)
                  }
                  onExport={(format) => handleExport(fileObj.id, format)}
                />
              ))
            )}
          </section>
        </div>
      </main>
    </div>
  )
}

export default App

