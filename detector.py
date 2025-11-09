import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import cv2
import numpy as np
from model import DeepfakeDetector, DeepfakeDetectorEfficientNet, SimpleDeepfakeDetector, CNNLSTMDeepfakeDetector

class DeepfakeDetectorInference:
    """
    Deepfake Detector for inference on images and videos
    """
    def __init__(self, model_path='deepfake_detector_best.pth', device=None):
        """
        Initialize the detector
        
        Args:
            model_path: Path to the trained model weights
            device: Device to run inference on ('cuda' or 'cpu')
        """
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_path = model_path
        
        # Image preprocessing (128x128 for CNN-LSTM model)
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),  # Changed from 224 to 128 to match model
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        print(f"Loading model from {self.model_path}...")
        
        # Try to load the checkpoint
        # PyTorch 2.6+ requires weights_only=False for older checkpoints
        try:
            checkpoint = torch.load(self.model_path, map_location=self.device, weights_only=False)
        except TypeError:
            # Fallback for older PyTorch versions
            checkpoint = torch.load(self.model_path, map_location=self.device)
        
        # Try different model architectures
        models_to_try = [
            CNNLSTMDeepfakeDetector,  # Try this first as it matches your model
            DeepfakeDetector,
            DeepfakeDetectorEfficientNet,
            SimpleDeepfakeDetector
        ]
        
        loaded = False
        for model_class in models_to_try:
            try:
                # Try num_classes=1 for CNN-LSTM, num_classes=2 for others
                num_classes = 1 if model_class == CNNLSTMDeepfakeDetector else 2
                self.model = model_class(num_classes=num_classes).to(self.device)
                
                # Handle different checkpoint formats
                if isinstance(checkpoint, dict):
                    if 'model_state_dict' in checkpoint:
                        self.model.load_state_dict(checkpoint['model_state_dict'])
                    elif 'state_dict' in checkpoint:
                        self.model.load_state_dict(checkpoint['state_dict'])
                    else:
                        self.model.load_state_dict(checkpoint)
                else:
                    self.model.load_state_dict(checkpoint)
                
                self.model.eval()
                print(f"✓ Model loaded successfully using {model_class.__name__}")
                loaded = True
                break
            except Exception as e:
                print(f"Failed to load with {model_class.__name__}: {str(e)}")
                continue
        
        if not loaded:
            raise Exception("Could not load model with any of the available architectures. Please check your model file.")
    
    def predict_image(self, image_path):
        """
        Predict if an image is a deepfake
        
        Args:
            image_path: Path to the image file or PIL Image object
            
        Returns:
            dict: Prediction results with probabilities
        """
        # Load image
        if isinstance(image_path, str):
            image = Image.open(image_path).convert('RGB')
        else:
            image = image_path.convert('RGB')
        
        # Preprocess
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # Predict
        with torch.no_grad():
            outputs = self.model(image_tensor)
            
            # Check if model outputs single value (sigmoid) or two values (softmax)
            if outputs.shape[1] == 1:
                # Single output with sigmoid
                fake_prob = torch.sigmoid(outputs[0][0]).item()
                real_prob = 1 - fake_prob
                prediction = 1 if fake_prob > 0.5 else 0
            else:
                # Two outputs with softmax
                probabilities = F.softmax(outputs, dim=1)
                prediction = torch.argmax(probabilities, dim=1).item()
                real_prob = probabilities[0][0].item()
                fake_prob = probabilities[0][1].item()
        
        return {
            'prediction': 'FAKE' if prediction == 1 else 'REAL',
            'confidence': max(real_prob, fake_prob) * 100,
            'real_probability': real_prob * 100,
            'fake_probability': fake_prob * 100,
            'is_deepfake': prediction == 1
        }
    
    def predict_video(self, video_path, num_frames=30, threshold=0.5):
        """
        Predict if a video contains deepfakes by analyzing multiple frames
        
        Args:
            video_path: Path to the video file
            num_frames: Number of frames to analyze
            threshold: Threshold for deepfake detection
            
        Returns:
            dict: Prediction results with frame-by-frame analysis
        """
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames == 0:
            raise ValueError("Could not read video file")
        
        # Sample frames evenly throughout the video
        frame_indices = np.linspace(0, total_frames - 1, min(num_frames, total_frames), dtype=int)
        
        predictions = []
        fake_count = 0
        
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                continue
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # Predict
            result = self.predict_image(pil_image)
            predictions.append(result)
            
            if result['is_deepfake']:
                fake_count += 1
        
        cap.release()
        
        # Calculate overall statistics
        avg_fake_prob = np.mean([p['fake_probability'] for p in predictions])
        fake_ratio = fake_count / len(predictions)
        
        overall_prediction = 'FAKE' if fake_ratio > threshold else 'REAL'
        
        return {
            'prediction': overall_prediction,
            'confidence': max(avg_fake_prob, 100 - avg_fake_prob),
            'fake_probability': avg_fake_prob,
            'real_probability': 100 - avg_fake_prob,
            'is_deepfake': fake_ratio > threshold,
            'frames_analyzed': len(predictions),
            'fake_frames': fake_count,
            'fake_ratio': fake_ratio * 100,
            'frame_predictions': predictions
        }
    
    def predict(self, file_path):
        """
        Automatically detect file type and predict
        
        Args:
            file_path: Path to image or video file
            
        Returns:
            dict: Prediction results
        """
        # Check file extension
        extension = file_path.lower().split('.')[-1]
        
        if extension in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
            return self.predict_image(file_path)
        elif extension in ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']:
            return self.predict_video(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python detector.py <image_or_video_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Initialize detector
    detector = DeepfakeDetectorInference('deepfake_detector_best.pth')
    
    # Make prediction
    result = detector.predict(file_path)
    
    # Print results
    print("\n" + "="*50)
    print("DEEPFAKE DETECTION RESULTS")
    print("="*50)
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2f}%")
    print(f"Real Probability: {result['real_probability']:.2f}%")
    print(f"Fake Probability: {result['fake_probability']:.2f}%")
    
    if 'frames_analyzed' in result:
        print(f"\nFrames Analyzed: {result['frames_analyzed']}")
        print(f"Fake Frames: {result['fake_frames']}")
        print(f"Fake Ratio: {result['fake_ratio']:.2f}%")
    
    print("="*50)
