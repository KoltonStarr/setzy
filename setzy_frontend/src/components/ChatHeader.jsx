import { useState } from 'react'
import './ChatHeader.css'

function ChatHeader({
  fileName,
  status,
  statusColor,
  isMinimized,
  onToggleMinimize,
  onExport,
  canExport,
}) {
  const [showExportMenu, setShowExportMenu] = useState(false)

  const handleExportClick = (format) => {
    onExport(format)
    setShowExportMenu(false)
  }

  const truncatedName =
    fileName.length > 30 ? `${fileName.substring(0, 30)}...` : fileName

  return (
    <div className="chat-header">
      <div className="chat-header-left">
        <button
          className="chat-header-toggle"
          onClick={onToggleMinimize}
          aria-label={isMinimized ? 'Expand' : 'Minimize'}
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className={isMinimized ? 'rotated' : ''}
          >
            <polyline points="18 15 12 9 6 15"></polyline>
          </svg>
        </button>
        <div className="chat-header-info">
          <h3 className="chat-header-title" title={fileName}>
            {truncatedName}
          </h3>
          <div
            className="chat-header-status"
            style={{ '--status-color': statusColor }}
          >
            <span className="status-dot"></span>
            <span className="status-text">{status}</span>
          </div>
        </div>
      </div>
      {canExport && (
        <div className="chat-header-actions">
          <div className="export-menu-container">
            <button
              className="chat-header-export"
              onClick={() => setShowExportMenu(!showExportMenu)}
              aria-label="Export"
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
            </button>
            {showExportMenu && (
              <>
                <div
                  className="export-menu-overlay"
                  onClick={() => setShowExportMenu(false)}
                />
                <div className="export-menu">
                  <button
                    className="export-menu-item"
                    onClick={() => handleExportClick('txt')}
                  >
                    Export as TXT
                  </button>
                  <button
                    className="export-menu-item"
                    onClick={() => handleExportClick('json')}
                  >
                    Export as JSON
                  </button>
                  <button
                    className="export-menu-item"
                    onClick={() => handleExportClick('csv')}
                  >
                    Export as CSV
                  </button>
                  <button
                    className="export-menu-item"
                    onClick={() => handleExportClick('md')}
                  >
                    Export as Markdown
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default ChatHeader


