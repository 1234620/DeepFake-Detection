import React from 'react'
import { Upload, Zap, Shield, Gauge } from 'lucide-react'

const Features = () => {
  const features = [
    {
      icon: Upload,
      title: 'Easy Upload',
      description: 'Upload images or videos in various formats. Supports PNG, JPG, MP4, and more.',
    },
    {
      icon: Zap,
      title: 'Fast Detection',
      description: 'Advanced AI models analyze your media in seconds.',
    },
    {
      icon: Shield,
      title: 'Secure Processing',
      description: 'Your files are processed securely and never stored.',
    },
    {
      icon: Gauge,
      title: 'Confidence Scores',
      description: 'Get detailed confidence metrics for detection results.',
    },
  ]

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Why Use Our Detector?</h2>
      <div className="space-y-4">
        {features.map((feature, index) => {
          const Icon = feature.icon
          return (
            <div key={index} className="flex gap-4 p-4 rounded-lg hover:bg-gray-50 transition">
              <div className="flex-shrink-0">
                <Icon className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-800 mb-1">{feature.title}</h3>
                <p className="text-gray-600 text-sm">{feature.description}</p>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Features
