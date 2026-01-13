import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import './FileDropzone.css'

const ACCEPTED_AUDIO_TYPES = {
  'audio/mpeg': ['.mp3'],
  'audio/wav': ['.wav'],
  'audio/x-m4a': ['.m4a'],
  'audio/ogg': ['.ogg'],
  'audio/webm': ['.webm'],
  'audio/aac': ['.aac'],
  'audio/flac': ['.flac'],
  'audio/x-wav': ['.wav'],
  'video/mp4': ['.mp4'],
  'video/webm': ['.webm'],
  'video/quicktime': ['.mov'],
}

function FileDropzone({ onFilesAccepted, files = [] }) {
  const onDrop = useCallback(
    (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onFilesAccepted(acceptedFiles)
      }
    },
    [onFilesAccepted]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_AUDIO_TYPES,
    multiple: true,
  })

  const processedCount = files.filter((f) => f.status === 'completed').length
  const processingCount = files.filter(
    (f) => f.status === 'uploading' || f.status === 'transcribing'
  ).length

  const getStatusIcon = (status) => {
    switch (status) {
      case 'uploading':
      case 'transcribing':
        return (
          <svg
            className="file-status-icon processing"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 6v6l4 2"></path>
          </svg>
        )
      case 'completed':
        return (
          <svg
            className="file-status-icon completed"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        )
      case 'error':
        return (
          <svg
            className="file-status-icon error"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        )
      default:
        return null
    }
  }

  return (
    <div className="file-dropzone-container">
      <h2 className="dropzone-title">Upload Audio Files</h2>
      <div
        {...getRootProps()}
        className={`file-dropzone ${isDragActive ? 'drag-active' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="dropzone-content">
          <svg
            className="dropzone-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          {isDragActive ? (
            <p className="dropzone-text">Drop files here...</p>
          ) : (
            <>
              <p className="dropzone-text">
                Drag & drop audio files here, or click to select
              </p>
              <p className="dropzone-subtext">
                Supports MP3, WAV, M4A, OGG, WebM, AAC, FLAC, MP4, MOV
              </p>
            </>
          )}
        </div>
      </div>
      {files.length > 0 && (
        <div className="file-status-section">
          <div className="file-status-summary">
            <span className="file-count-text">
              {files.length} file{files.length !== 1 ? 's' : ''} uploaded
            </span>
            {processedCount > 0 && (
              <span className="file-count-badge processed">
                {processedCount} processed
              </span>
            )}
            {processingCount > 0 && (
              <span className="file-count-badge processing">
                {processingCount} processing
              </span>
            )}
          </div>
          <div className="file-status-icons">
            {files.map((file) => (
              <div
                key={file.id}
                className="file-status-item"
                title={file.name}
              >
                {getStatusIcon(file.status)}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default FileDropzone


