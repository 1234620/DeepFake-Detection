from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import sys
from detector import DeepfakeDetectorInference
import traceback
from flask_cors import CORS

# Determine if we're in production
IS_PRODUCTION = os.getenv('RENDER') is not None or os.getenv('ENVIRONMENT') == 'production'

# Setup Flask app with static files for production
if IS_PRODUCTION:
    app = Flask(__name__, static_folder='dist', static_url_path='')
else:
    app = Flask(__name__)

# Enable CORS for development
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration
UPLOAD_FOLDER = '/tmp/uploads' if IS_PRODUCTION else 'uploads'
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
    if IS_PRODUCTION:
        return send_from_directory('dist', 'index.html')
    else:
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
        # Add timestamp to prevent collisions
        import time
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Perform detection
        detection_result = detector.predict(filepath)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'is_deepfake': detection_result.get('is_deepfake', False),
            'confidence': detection_result.get('confidence', 0),
            'processing_time': detection_result.get('processing_time', 0),
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


@app.errorhandler(404)
def not_found(e):
    """Serve index.html for all non-API routes (SPA fallback)"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    if IS_PRODUCTION:
        return send_from_directory('dist', 'index.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting Deepfake Detection Server")
    print("="*60)
    
    port = int(os.getenv('PORT', 5000))
    debug = not IS_PRODUCTION
    
    print(f"Server will be available at: http://0.0.0.0:{port}")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Max file size: {MAX_FILE_SIZE / (1024*1024):.0f}MB")
    print(f"Production mode: {IS_PRODUCTION}")
    print("="*60 + "\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
