import sys
sys.path.append('..')
import torch
from deepfake_model import DeepfakeDetector
from deepfake_dataset import is_image_file, is_video_file
from torchvision import transforms
from PIL import Image
import cv2
import time
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {DEVICE}")

# Preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

# Load the trained model
print("Loading model...")
model = DeepfakeDetector(use_lstm=True, T=16)
model.load_state_dict(torch.load('../deepfake_detector.pth', map_location=DEVICE))
model.eval()
model.to(DEVICE)
print("Model loaded successfully")

def infer_image(path):
    start_time = time.time()
    img = Image.open(path).convert('RGB')
    img = transform(img)
    img = img.unsqueeze(0)
    with torch.no_grad():
        prob = model(img.to(DEVICE), 'image').item()
    inference_time = time.time() - start_time
    return prob, inference_time

def extract_frames(video_path, T=16):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = frame_count / T
    frames = []
    for i in range(T):
        idx = int(i * step)
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frames.append(frame)
    cap.release()
    while len(frames) < T:
        frames.append(frames[-1].copy())
    return frames[:T]

def infer_video(path):
    start_time = time.time()
    frames = extract_frames(path, T=16)
    frames = torch.stack([transform(f) for f in frames], dim=0)
    with torch.no_grad():
        prob = model(frames.to(DEVICE), 'video').item()
    inference_time = time.time() - start_time
    return prob, inference_time

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    path = data.get('path')
    if not path or not os.path.exists(path):
        return jsonify({'error': 'Invalid file path'}), 400

    try:
        if is_image_file(path):
            prob, inf_time = infer_image(path)
            is_fake = prob >= 0.5
            result = 'FAKE' if is_fake else 'REAL'
            # For REAL results: show the model's fake probability (how fake it thinks it is)
            # For FAKE results: show the model's fake probability (how fake it thinks it is)
            confidence = prob  # Always show the raw fake probability from the model
            confidence_label = 'Low Fake Probability' if not is_fake else 'High Fake Probability'
            return jsonify({
                'result': result,
                'confidence': f"{confidence:.4f}",
                'confidence_label': confidence_label,
                'inference_time': f"{inf_time:.2f}s",
                'raw_probability': prob
            })
        elif is_video_file(path):
            prob, inf_time = infer_video(path)
            is_fake = prob >= 0.5
            result = 'FAKE' if is_fake else 'REAL'
            # For REAL results: show the model's fake probability (how fake it thinks it is)
            # For FAKE results: show the model's fake probability (how fake it thinks it is)
            confidence = prob  # Always show the raw fake probability from the model
            confidence_label = 'Low Fake Probability' if not is_fake else 'High Fake Probability'
            return jsonify({
                'result': result,
                'confidence': f"{confidence:.4f}",
                'confidence_label': confidence_label,
                'inference_time': f"{inf_time:.2f}s",
                'raw_probability': prob
            })
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)