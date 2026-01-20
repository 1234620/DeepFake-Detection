# Deepfake Detector Web UI

A Node.js + Express web interface for detecting deepfakes using a PyTorch model.

## Prerequisites

- Node.js (v14 or higher)
- Python (with PyTorch and required dependencies for detect.py)

## Installation

1. Navigate to the `ui` folder:
   ```
   cd ui
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Application

For development (with auto-restart):
```
npm run dev
```

For production:
```
npm start
```

The server will start on http://localhost:3001

## Usage

1. Open your browser and go to http://localhost:3001
2. Upload an image or video file
3. Click "Detect" to analyze the file
4. View the result with appropriate confidence level

### Confidence Display Logic

- **REAL images**: Shows "Probability of Being Real" = 1 - fake_probability
- **FAKE images**: Shows "Probability of Being Fake" = fake_probability
- **Progress bar**: Visual representation of the displayed probability
- **Raw probability**: Model's original fake probability available in API

## API Endpoint

- POST `/detect`: Accepts a file upload and returns detection result as JSON

## File Structure

- `server.js`: Express server with file upload and detection logic
- `public/index.html`: Frontend HTML
- `public/style.css`: Stylesheet
- `public/script.js`: Frontend JavaScript
- `uploads/`: Temporary storage for uploaded files