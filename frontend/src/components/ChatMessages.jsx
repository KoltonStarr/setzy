import './ChatMessages.css'

function ChatMessages({ messages }) {
  if (messages.length === 0) {
    return (
      <div className="chat-messages-empty">
        <p>Start a conversation about this transcript</p>
      </div>
    )
  }

  return (
    <div className="chat-messages">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`chat-message chat-message-${message.role}`}
        >
          <div className="chat-message-content">
            <div className="chat-message-header">
              <span className="chat-message-role">
                {message.role === 'user' ? 'You' : 'Assistant'}
              </span>
              <span className="chat-message-time">
                {new Date(message.timestamp).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </span>
            </div>
            <div className="chat-message-text">{message.content}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ChatMessages


