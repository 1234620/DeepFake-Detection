import React from 'react'

const Header = () => {
  return (
    <nav className="bg-blue-900 shadow-lg">
      <div className="max-w-6xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
              <span className="text-blue-600 font-bold text-lg">🔍</span>
            </div>
            <h1 className="text-white text-xl font-bold">DeepFake Detector</h1>
          </div>
          <div className="flex gap-6">
            <a href="#" className="text-blue-100 hover:text-white transition">Home</a>
            <a href="#features" className="text-blue-100 hover:text-white transition">Features</a>
            <a href="#about" className="text-blue-100 hover:text-white transition">About</a>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Header
