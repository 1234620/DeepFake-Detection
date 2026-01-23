#!/usr/bin/env bash
set -o errexit

echo "📦 Installing Node dependencies..."
npm install

echo "🏗️  Building TypeScript frontend..."
npm run build

echo "✅ Build complete! Frontend ready in ./dist directory"
echo ""
echo "Next steps:"
echo "1. Ensure Python dependencies are installed: pip install -r requirements.txt"
echo "2. Start the backend: python app.py"
echo "3. Or deploy to Render using Procfile configuration"
