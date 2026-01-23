import React, { useCallback } from 'react'
import { Cloud } from 'lucide-react'

interface FileUploadProps {
  onFileUpload: (file: File) => void
  isLoading: boolean
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload, isLoading }) => {
  const [dragActive, setDragActive] = React.useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      onFileUpload(files[0])
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files[0]) {
      onFileUpload(files[0])
    }
  }

  return (
    <div
      className={`upload-area rounded-xl p-8 text-center cursor-pointer transition ${
        dragActive ? 'drag-active' : ''
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        id="file-input"
        onChange={handleChange}
        disabled={isLoading}
        className="hidden"
        accept="image/*,video/*"
      />

      <label htmlFor="file-input" className="cursor-pointer">
        {isLoading ? (
          <div className="flex justify-center">
            <div className="loader"></div>
          </div>
        ) : (
          <>
            <Cloud className="w-16 h-16 mx-auto text-blue-500 mb-4" />
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Drop your file here
            </h3>
            <p className="text-gray-600 mb-4">or click to browse</p>
            <p className="text-sm text-gray-500">
              Supports: PNG, JPG, GIF, BMP, MP4, AVI, MOV, MKV (Max 100MB)
            </p>
          </>
        )}
      </label>
    </div>
  )
}

export default FileUpload
