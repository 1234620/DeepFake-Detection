import React from 'react'
import { AlertCircle, CheckCircle } from 'lucide-react'

interface DetectionResult {
  success: boolean
  is_deepfake: boolean
  confidence: number
  processing_time: number
  error?: string
}

interface DetectionResultProps {
  result: DetectionResult
}

const DetectionResult: React.FC<DetectionResultProps> = ({ result }) => {
  const confidencePercentage = Math.round(result.confidence * 100)
  
  return (
    <div className="result-card bg-gradient-to-br from-blue-50 to-white rounded-lg p-6 border border-blue-200">
      <div className="flex items-start gap-4 mb-4">
        {result.is_deepfake ? (
          <AlertCircle className="w-8 h-8 text-red-500 flex-shrink-0 mt-1" />
        ) : (
          <CheckCircle className="w-8 h-8 text-green-500 flex-shrink-0 mt-1" />
        )}
        <div>
          <h3 className="text-lg font-bold text-gray-800">
            {result.is_deepfake ? 'Deepfake Detected' : 'Authentic Media'}
          </h3>
          <p className={`text-sm ${result.is_deepfake ? 'text-red-600' : 'text-green-600'}`}>
            {result.is_deepfake 
              ? 'This media appears to be manipulated or artificially generated.' 
              : 'This media appears to be authentic.'}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-lg p-4 mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="font-semibold text-gray-700">Confidence Score</span>
          <span className="text-2xl font-bold text-blue-600">{confidencePercentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all ${
              result.is_deepfake ? 'bg-red-500' : 'bg-green-500'
            }`}
            style={{ width: `${confidencePercentage}%` }}
          ></div>
        </div>
      </div>

      <div className="text-sm text-gray-600">
        <p>Processing time: <span className="font-semibold">{result.processing_time.toFixed(2)}s</span></p>
      </div>
    </div>
  )
}

export default DetectionResult
