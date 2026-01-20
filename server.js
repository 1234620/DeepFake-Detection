const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

const app = express();

// Enable CORS for all routes
app.use(cors());

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Configure Multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // Ensure uploads directory exists
    const uploadDir = 'uploads/';
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    // Generate unique filename with original extension
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    const extension = path.extname(file.originalname);
    cb(null, file.fieldname + '-' + uniqueSuffix + extension);
  }
});

const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    // Accept only image and video files
    if (file.mimetype.startsWith('image/') || file.mimetype.startsWith('video/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image and video files are allowed!'), false);
    }
  },
  limits: {
    fileSize: 50 * 1024 * 1024, // 50MB limit
  }
});

// POST endpoint for detection
app.post('/detect', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  const filePath = req.file.path;
  console.log('Processing file:', filePath);

  // Check if file exists
  if (!fs.existsSync(filePath)) {
    console.error('File does not exist:', filePath);
    return res.status(500).json({ error: 'File upload failed' });
  }

  // Run the Python detection script
  const pythonProcess = spawn('python', ['../detect.py', filePath]);

  let output = '';
  let errorOutput = '';

  // Collect stdout
  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  // Collect stderr
  pythonProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  // Handle process close
  pythonProcess.on('close', (code) => {
    console.log('Python process exited with code:', code);
    console.log('Output:', output);
    console.log('Error output:', errorOutput);

    // Check for unsupported file type first
    if (output.includes('Unsupported file type.')) {
      return res.status(400).json({ error: 'Unsupported file type. Please upload a JPG, PNG, MP4, AVI, or MOV file.' });
    }

    // Check for errors
    if (output.includes('Error:')) {
      const errorMatch = output.match(/Error: (.+)/);
      return res.status(500).json({ error: errorMatch ? errorMatch[1] : 'An error occurred during detection' });
    }

    if (code !== 0) {
      console.error(`Python script exited with code ${code}`);
      console.error(`Error output: ${errorOutput}`);
      return res.status(500).json({ error: 'Error running detection script' });
    }

    // Extract the probability from the output
    const match = output.match(/(Image|Video) probability \(fake\): (\d+\.\d+)/);
    if (!match) {
      console.error('Could not parse output:', output);
      return res.status(500).json({ error: 'Could not parse detection output' });
    }

    const prob = parseFloat(match[2]);
    const result = prob >= 0.5 ? 'FAKE' : 'REAL';
    const confidence = result === 'FAKE' ? (prob * 100).toFixed(2) + '%' : ((1 - prob) * 100).toFixed(2) + '%';
    const confidence_label = result === 'FAKE' ? 'Probability of Being Fake' : 'Probability of Being Real';

    // Return JSON response
    res.json({
      result: result,
      confidence: confidence,
      confidence_label: confidence_label
    });
  });

  // Handle process error
  pythonProcess.on('error', (error) => {
    console.error('Failed to start Python process:', error);
    res.status(500).json({ error: 'Failed to start detection script' });
  });
});

// Start the server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});