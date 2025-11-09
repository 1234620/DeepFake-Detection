from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from detector import DeepfakeDetectorInference
import traceback

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the detector
try:
    detector = DeepfakeDetectorInference('deepfake_detector_best.pth')
    print("✓ Deepfake detector initialized successfully!")
except Exception as e:
    print(f"✗ Error initializing detector: {str(e)}")
    detector = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/detect', methods=['POST'])
def detect():
    """API endpoint for deepfake detection"""
    if detector is None:
        return jsonify({
            'success': False,
            'error': 'Detector not initialized. Please check if the model file exists.'
        }), 500
    
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file uploaded'
        }), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'Invalid file format. Allowed formats: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Perform detection
        result = detector.predict(filepath)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        print(f"Error during detection: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error processing file: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if detector is not None else 'unhealthy',
        'model_loaded': detector is not None
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Deepfake Detection Server")
    print("="*60)
    print(f"Server will be available at: http://localhost:5000")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Max file size: {MAX_FILE_SIZE / (1024*1024):.0f}MB")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
