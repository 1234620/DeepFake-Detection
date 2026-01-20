// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const preview = document.getElementById('preview');
const detectBtn = document.getElementById('detectBtn');
const resultCard = document.getElementById('resultCard');
const resultBadge = document.getElementById('resultBadge');
const resultText = document.getElementById('resultText');
const confidenceValue = document.getElementById('confidenceValue');
const progressFill = document.getElementById('progressFill');
const toast = document.getElementById('toast');

// Drag & Drop functionality
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
  uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadArea.classList.remove('dragover');
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFileSelect(files[0]);
  }
});

// File input change
fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    handleFileSelect(e.target.files[0]);
  }
});

// Handle file selection
function handleFileSelect(file) {
  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'video/mp4', 'video/avi', 'video/quicktime'];
  if (!allowedTypes.includes(file.type)) {
    showToast('Please select a valid image (JPG, PNG) or video (MP4, AVI, MOV) file.');
    return;
  }

  // Clear previous results
  resultCard.classList.add('hidden');
  resultCard.classList.remove('real', 'fake');

  // Preview file
  previewFile(file);

  // Enable detect button
  detectBtn.disabled = false;
}

// Preview the selected file
function previewFile(file) {
  preview.classList.remove('hidden');
  preview.innerHTML = '';

  const url = URL.createObjectURL(file);

  if (file.type.startsWith('image/')) {
    const img = document.createElement('img');
    img.src = url;
    img.onload = () => URL.revokeObjectURL(url);
    preview.appendChild(img);
  } else if (file.type.startsWith('video/')) {
    const video = document.createElement('video');
    video.src = url;
    video.controls = true;
    video.preload = 'metadata';
    video.onloadedmetadata = () => URL.revokeObjectURL(url);
    preview.appendChild(video);
  }
}

// Detect button click
detectBtn.addEventListener('click', async () => {
  const file = fileInput.files[0];
  if (!file) return;

  // Disable button and show loading
  detectBtn.disabled = true;
  detectBtn.textContent = 'Analyzing...';

  // Show result card with loading state
  resultCard.classList.remove('hidden');
  resultCard.classList.add('loading');
  resultText.textContent = 'Analyzing...';
  confidenceValue.textContent = '0%';
  progressFill.style.width = '0%';

  try {
    // Prepare FormData
    const formData = new FormData();
    formData.append('file', file);

    // Send request
    const response = await fetch('/detect', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    console.log('Response data:', data);

    if (data.error) {
      showToast(data.error);
      resultCard.classList.add('hidden');
    } else {
      // Update result
      displayResult(data.result, data.confidence, data.inference_time, data.confidence_label);
    }
  } catch (error) {
    console.error('Error:', error);
    showToast('An error occurred while processing the file. Please try again.');
    resultCard.classList.add('hidden');
  }

  // Re-enable button
  detectBtn.disabled = false;
  detectBtn.textContent = 'Detect Deepfake';
});

// Display detection result
function displayResult(result, confidence, inferenceTime, confidenceLabel) {
  console.log('Displaying result:', result, 'confidence:', confidence, 'label:', confidenceLabel, 'time:', inferenceTime);
  resultCard.classList.remove('loading');

  const isReal = result === 'REAL';
  resultCard.classList.add(isReal ? 'real' : 'fake');

  resultText.textContent = result;
  confidenceValue.textContent = confidence;

  // Update confidence label from server response
  const confidenceLabelElement = document.querySelector('.confidence-label span:first-child');
  confidenceLabelElement.textContent = confidenceLabel || (isReal ? 'Probability of Being Real' : 'Probability of Being Fake');

  // Animate progress bar (convert to percentage for visual representation)
  const confidenceNum = parseFloat(confidence);
  const percentage = confidenceNum * 100;
  console.log('Setting progress to:', percentage + '%');
  progressFill.style.width = `${percentage}%`;

  // Show inference time if available
  if (inferenceTime) {
    const timeElement = document.createElement('p');
    timeElement.textContent = `Analysis time: ${inferenceTime}`;
    timeElement.style.fontSize = '0.9rem';
    timeElement.style.opacity = '0.8';
    timeElement.style.marginTop = '1rem';
    resultCard.appendChild(timeElement);
  }
}

// Show toast notification
function showToast(message) {
  toast.textContent = message;
  toast.classList.remove('hidden');

  setTimeout(() => {
    toast.classList.add('hidden');
  }, 4000);
}

// Highlight text click
document.querySelector('.highlight').addEventListener('click', () => {
  fileInput.click();
});