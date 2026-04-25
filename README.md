<div align="center">

# DEEPFAKE DETECTION SYSTEM

*Detecting Manipulation, Preserving Truth, Securing Authenticity*

![Last Commit](https://img.shields.io/badge/last_commit-September_2025-blue?style=flat-square)
![Top Language](https://img.shields.io/badge/top_language-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Languages](https://img.shields.io/badge/languages-4-orange?style=flat-square)

<br>

*Built with the tools and technologies:*

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
<br>
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

</div>

<br>
<hr>

##  Features

### Core Functionality
- **Image Analysis**: Single-image deepfake detection with probability scores
- **Video Analysis**: Frame-by-frame video analysis with temporal consistency checking
- **Batch Processing**: Support for multiple file formats and sizes
- **Real-time Inference**: Fast prediction with GPU acceleration support

### Technical Capabilities
- **CNN-LSTM Architecture**: Combines convolutional feature extraction with temporal sequence analysis
- **Binary Classification**: Outputs probability scores for real vs. fake content
- **Flexible Input**: Accepts images (128x128) and videos with automatic preprocessing
- **Multiple Architecture Support**: Compatible with ResNet50, EfficientNet, and custom CNN models

### User Interface
- Web-based interface with drag-and-drop functionality
- REST API for programmatic access
- Command-line interface for batch processing
- Detailed confidence scores and frame-level analysis for videos

##  Installation and Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager
- (Optional) CUDA-compatible GPU for faster inference

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd deepfake
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify model file exists:**
   ```bash
   # Ensure deepfake_detector_best.pth is in the project directory
   ```

##  Running the Application

### Web Interface
```bash
python app.py
```
Access the application at `http://localhost:5000`

### Command Line Interface
```bash
# For single image
python detector.py path/to/image.jpg

# For video
python detector.py path/to/video.mp4
```

### Model Evaluation (CLI)
```bash
# Evaluate on test dataset
python evaluate.py --test_data path/to/test_dataset

# Test single image
python evaluate.py --image path/to/image.jpg
```

##  Project Structure

```
deepfake/
├── app.py                          # Flask web server and API endpoints
├── detector.py                     # Core detection inference engine
├── model.py                        # Neural network architecture definitions
├── evaluate.py                     # Model evaluation and testing utilities
├── deepfake_detector_best.pth      # Pre-trained model weights (CNN-LSTM)
├── requirements.txt                # Python package dependencies
├── README.md                       # Project documentation
├── templates/
│   └── index.html                  # Frontend web interface
└── uploads/                        # Temporary file storage (auto-generated)
```

##  Model Architecture

### CNN-LSTM Architecture (Primary Model)
The current implementation uses a hybrid CNN-LSTM architecture optimized for deepfake detection:

**Convolutional Neural Network (Feature Extraction)**
- 3 Convolutional layers: 3→32→64→128 channels
- MaxPooling after each convolution (2x2)
- Input size: 128x128x3 RGB images
- Feature compression to 512-dimensional vector

**Long Short-Term Memory (Temporal Analysis)**
- Bidirectional LSTM with 2 layers
- Hidden size: 256 units per direction
- Captures temporal inconsistencies in video sequences

**Classification Head**
- Fully connected layers: 512→128→1
- Sigmoid activation for binary classification
- Dropout (0.5) for regularization

### Alternative Architectures Supported
1. **ResNet50**: Transfer learning with custom classifier head
2. **EfficientNet-B0**: Lightweight architecture for resource-constrained environments
3. **Simple CNN**: Basic convolutional network for baseline comparisons

The system automatically detects and loads the appropriate architecture based on the checkpoint file.

##  API Response Format

### Image Detection Response
```json
{
  "success": true,
  "result": {
    "prediction": "FAKE",
    "confidence": 95.5,
    "real_probability": 4.5,
    "fake_probability": 95.5,
    "is_deepfake": true
  }
}
```

### Video Detection Response
```json
{
  "success": true,
  "result": {
    "prediction": "FAKE",
    "confidence": 87.3,
    "fake_probability": 87.3,
    "real_probability": 12.7,
    "is_deepfake": true,
    "frames_analyzed": 30,
    "fake_frames": 26,
    "fake_ratio": 86.7,
    "frame_predictions": [...]
  }
}
```

##  API Endpoints

### POST /api/detect
Upload and analyze an image or video file.

**Request**: multipart/form-data with 'file' field

**Response**: JSON with prediction results

### GET /api/health
Check server and model status.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```
this is the change 
##  Configuration and Customization

### Model Configuration
**Change model checkpoint path** (app.py or detector.py):
```python
detector = DeepfakeDetectorInference('path/to/custom_model.pth')
```

**Modify image preprocessing**:
```python
# In detector.py, adjust transform parameters
self.transform = transforms.Compose([
    transforms.Resize((128, 128)),  # Input size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                        std=[0.229, 0.224, 0.225])
])
```

### Video Analysis Parameters
**Adjust frame sampling**:
```python
result = detector.predict_video(
    video_path, 
    num_frames=50,      # Number of frames to analyze
    threshold=0.6       # Classification threshold (default: 0.5)
)
```

### Server Configuration
**Modify Flask settings** (app.py):
```python
# Change port
app.run(debug=True, host='0.0.0.0', port=5001)

# Adjust file size limit
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

# Add allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'webm'}
```

##  Performance Optimization

### GPU Acceleration
The system automatically detects and uses CUDA-compatible GPUs:
```python
# Force CPU usage
detector = DeepfakeDetectorInference(device=torch.device('cpu'))

# Force GPU usage
detector = DeepfakeDetectorInference(device=torch.device('cuda'))
```

### Batch Processing
For processing multiple files, use the command-line interface in a loop or modify the detector for batch inference.

### Memory Management
- Video processing uses frame sampling to reduce memory footprint
- Temporary files are automatically cleaned up after processing
- Adjust `num_frames` parameter for videos based on available RAM

##  Model Evaluation

To evaluate the model on a test dataset:

```bash
python evaluate.py --test_data path/to/test_dataset --batch_size 32
```

**Expected test dataset structure**:
```
test_dataset/
├── real/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── fake/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

**Evaluation outputs**:
- Overall accuracy, precision, recall, F1-score
- Per-class performance metrics
- Confusion matrix (saved as PNG)
- Detailed classification report

##  Troubleshooting

### Common Issues

**PyTorch Version Compatibility**
```bash
# Error: weights_only parameter issue
# Solution: The code handles PyTorch 2.6+ automatically
# If issues persist, use: weights_only=False in torch.load()
```

**Model Architecture Mismatch**
```
Error: Missing keys or unexpected keys in state_dict
Solution: 
1. Verify the checkpoint file is not corrupted
2. Ensure model.py architecture matches training architecture
3. Check num_classes parameter (1 for sigmoid, 2 for softmax)
```

**CUDA Out of Memory**
```python
# Reduce batch size or use CPU
detector = DeepfakeDetectorInference(device=torch.device('cpu'))

# For videos, reduce frame count
result = detector.predict_video(video_path, num_frames=10)
```

**Port Already in Use**
```bash
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

##  Technical Specifications

### Supported File Formats
- **Images**: JPG, JPEG, PNG, GIF, BMP
- **Videos**: MP4, AVI, MOV, MKV, FLV, WMV

### System Requirements
- **Minimum RAM**: 4GB (8GB recommended for video processing)
- **Storage**: 500MB for dependencies + model weights
- **GPU**: Optional, NVIDIA GPU with CUDA support for acceleration

### Performance Metrics
- **Image Inference**: ~50-200ms per image (CPU), ~10-50ms (GPU)
- **Video Processing**: Depends on frame count and resolution
- **Model Size**: ~100-200MB depending on architecture

##  Development and Contributing

### Code Structure
- **model.py**: Define new architectures or modify existing ones
- **detector.py**: Core inference logic and preprocessing
- **app.py**: API endpoints and server configuration
- **evaluate.py**: Testing and validation utilities

### Adding New Model Architectures
1. Define architecture class in `model.py`
2. Add to `models_to_try` list in `detector.py`
3. Ensure forward pass returns correct output shape

### Testing
```bash
# Test model loading
python -c "from detector import DeepfakeDetectorInference; detector = DeepfakeDetectorInference('deepfake_detector_best.pth')"

# Test single prediction
python detector.py test_image.jpg
```

##  License

This project is provided as-is for educational and research purposes.

##  Acknowledgments

Built using PyTorch, Flask, and OpenCV for deep learning-based deepfake detection.
