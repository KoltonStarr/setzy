import { useState, useRef, useEffect } from 'react'
import ChatHeader from './ChatHeader'
import ChatMessages from './ChatMessages'
import ChatInput from './ChatInput'
import './ChatColumn.css'

function ChatColumn({ file, messages = [], isMinimized = false, onToggleMinimize, onAddMessage, onExport, isGeneralChat = false }) {
  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    if (!isMinimized) {
      scrollToBottom()
    }
  }, [messages, isMinimized])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue.trim()) {
      onAddMessage(inputValue.trim())
      setInputValue('')
    }
  }

  const getStatusColor = () => {
    if (isGeneralChat) {
      return 'var(--success)'
    }
    switch (file?.status) {
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
    if (isGeneralChat) {
      return 'Ready'
    }
    switch (file?.status) {
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

  const getFileName = () => {
    if (isGeneralChat) {
      return 'General Chat'
    }
    return file?.name || 'Unknown File'
  }

  const canChat = isGeneralChat || file?.status === 'completed'

  return (
    <div className={`chat-column ${isMinimized ? 'minimized' : ''}`}>
      <ChatHeader
        fileName={getFileName()}
        status={getStatusText()}
        statusColor={getStatusColor()}
        isMinimized={isMinimized}
        onToggleMinimize={onToggleMinimize}
        onExport={onExport}
        canExport={!isGeneralChat && file?.status === 'completed'}
      />
      {!isMinimized && (
        <div className="chat-column-content">
          <ChatMessages messages={messages} />
          <div ref={messagesEndRef} />
          {canChat && (
            <ChatInput
              value={inputValue}
              onChange={setInputValue}
              onSubmit={handleSubmit}
            />
          )}
          {!canChat && (
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


