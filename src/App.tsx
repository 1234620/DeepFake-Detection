import React, { useState } from 'react'
import FileUpload from './components/FileUpload'
import DetectionResult from './components/DetectionResult'
import Header from './components/Header'
import Features from './components/Features'
import { getConfig } from './config'

interface DetectionResponse {
  success: boolean
  is_deepfake: boolean
  confidence: number
  processing_time: number
  error?: string
}

function App() {
  const [result, setResult] = useState<DetectionResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const config = getConfig()

  const handleFileUpload = async (file: File) => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${config.apiUrl}/api/detect`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (data.success) {
        setResult(data)
      } else {
        setError(data.error || 'Detection failed')
      }
    } catch (err) {
      setError('Error connecting to server. Please try again.')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
  }

  return (
    <div className="gradient-bg min-h-screen">
      <Header />
      
      <main className="py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">
              AI-Powered Deepfake Detector
            </h1>
            <p className="text-xl text-blue-100 max-w-2xl mx-auto">
              Detect manipulated media with advanced AI technology. Upload an image or video to verify its authenticity and protect against disinformation.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8 mb-12">
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Upload Media</h2>
              <FileUpload onFileUpload={handleFileUpload} isLoading={isLoading} />
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              )}
              {result && (
                <div className="mt-4">
                  <DetectionResult result={result} />
                  <button
                    onClick={handleReset}
                    className="w-full mt-4 px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition"
                  >
                    Check Another File
                  </button>
                </div>
              )}
            </div>

            <div className="bg-white rounded-2xl shadow-xl p-8">
              <Features />
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-blue-900 text-white py-8">
        <div className="max-w-6xl mx-auto text-center">
          <p>&copy; 2024 DeepFake Detection. Protecting against media manipulation.</p>
        </div>
      </footer>
    </div>
  )
}

export default App
