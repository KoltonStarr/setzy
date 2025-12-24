import { useState, useRef, useEffect } from 'react'
import ChatHeader from './ChatHeader'
import ChatMessages from './ChatMessages'
import ChatInput from './ChatInput'
import './ChatColumn.css'

function ChatColumn({ file, onToggleMinimize, onAddMessage, onExport }) {
  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    if (!file.isMinimized) {
      scrollToBottom()
    }
  }, [file.messages, file.isMinimized])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue.trim()) {
      onAddMessage(inputValue.trim())
      setInputValue('')
    }
  }

  const getStatusColor = () => {
    switch (file.status) {
      case 'uploading':
        return 'var(--warning)'
      case 'transcribing':
        return 'var(--accent-primary)'
      case 'completed':
        return 'var(--success)'
      case 'error':
        return 'var(--error)'
      default:
        return 'var(--text-muted)'
    }
  }

  const getStatusText = () => {
    switch (file.status) {
      case 'uploading':
        return 'Uploading...'
      case 'transcribing':
        return 'Transcribing...'
      case 'completed':
        return 'Ready'
      case 'error':
        return 'Error'
      default:
        return 'Unknown'
    }
  }

  return (
    <div className={`chat-column ${file.isMinimized ? 'minimized' : ''}`}>
      <ChatHeader
        fileName={file.name}
        status={getStatusText()}
        statusColor={getStatusColor()}
        isMinimized={file.isMinimized}
        onToggleMinimize={onToggleMinimize}
        onExport={onExport}
        canExport={file.status === 'completed'}
      />
      {!file.isMinimized && (
        <div className="chat-column-content">
          <ChatMessages messages={file.messages} />
          <div ref={messagesEndRef} />
          {file.status === 'completed' && (
            <ChatInput
              value={inputValue}
              onChange={setInputValue}
              onSubmit={handleSubmit}
            />
          )}
          {file.status !== 'completed' && (
            <div className="chat-status-message">
              <div className="status-spinner"></div>
              <p>{getStatusText()}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ChatColumn


