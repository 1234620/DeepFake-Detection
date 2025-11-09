import torch
import torch.nn.functional as F
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from model import DeepfakeDetector, DeepfakeDetectorEfficientNet, SimpleDeepfakeDetector, CNNLSTMDeepfakeDetector

class ModelEvaluator:
    """
    Evaluate the deepfake detection model on a test dataset
    """
    def __init__(self, model_path='deepfake_detector_best.pth', device=None):
        """
        Initialize the evaluator
        
        Args:
            model_path: Path to the trained model weights
            device: Device to run evaluation on ('cuda' or 'cpu')
        """
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_path = model_path
        
        # Image preprocessing (same as training)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        print(f"Loading model from {self.model_path}...")
        
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
                continue
        
        if not loaded:
            raise Exception("Could not load model with any of the available architectures.")
    
    def evaluate_on_dataset(self, test_data_path, batch_size=32):
        """
        Evaluate model on a test dataset
        
        Args:
            test_data_path: Path to test dataset folder
                           Should have structure: test_data_path/real/ and test_data_path/fake/
            batch_size: Batch size for evaluation
            
        Returns:
            dict: Evaluation metrics
        """
        print(f"\n{'='*60}")
        print("Loading test dataset...")
        print(f"{'='*60}\n")
        
        # Load dataset
        try:
            test_dataset = datasets.ImageFolder(test_data_path, transform=self.transform)
            test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
            
            print(f"Test dataset loaded successfully!")
            print(f"Total samples: {len(test_dataset)}")
            print(f"Classes: {test_dataset.classes}")
            print(f"Class to index mapping: {test_dataset.class_to_idx}\n")
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            print("\nExpected folder structure:")
            print("test_data_path/")
            print("├── real/")
            print("│   ├── image1.jpg")
            print("│   ├── image2.jpg")
            print("│   └── ...")
            print("└── fake/")
            print("    ├── image1.jpg")
            print("    ├── image2.jpg")
            print("    └── ...")
            return None
        
        # Evaluate
        all_preds = []
        all_labels = []
        all_probs = []
        
        print("Evaluating model...")
        with torch.no_grad():
            for i, (images, labels) in enumerate(test_loader):
                images = images.to(self.device)
                labels = labels.to(self.device)
                
                outputs = self.model(images)
                probabilities = F.softmax(outputs, dim=1)
                predictions = torch.argmax(probabilities, dim=1)
                
                all_preds.extend(predictions.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                all_probs.extend(probabilities.cpu().numpy())
                
                if (i + 1) % 10 == 0:
                    print(f"Processed {(i + 1) * batch_size} / {len(test_dataset)} images...")
        
        all_preds = np.array(all_preds)
        all_labels = np.array(all_labels)
        all_probs = np.array(all_probs)
        
        # Calculate metrics
        metrics = self.calculate_metrics(all_labels, all_preds, all_probs)
        
        # Print results
        self.print_results(metrics, test_dataset.classes)
        
        # Plot confusion matrix
        self.plot_confusion_matrix(metrics['confusion_matrix'], test_dataset.classes)
        
        return metrics
    
    def calculate_metrics(self, labels, predictions, probabilities):
        """Calculate evaluation metrics"""
        accuracy = accuracy_score(labels, predictions)
        precision = precision_score(labels, predictions, average='binary')
        recall = recall_score(labels, predictions, average='binary')
        f1 = f1_score(labels, predictions, average='binary')
        
        # Per-class metrics
        precision_per_class = precision_score(labels, predictions, average=None)
        recall_per_class = recall_score(labels, predictions, average=None)
        f1_per_class = f1_score(labels, predictions, average=None)
        
        # Confusion matrix
        cm = confusion_matrix(labels, predictions)
        
        # Classification report
        report = classification_report(labels, predictions, target_names=['Real', 'Fake'])
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'precision_per_class': precision_per_class,
            'recall_per_class': recall_per_class,
            'f1_per_class': f1_per_class,
            'confusion_matrix': cm,
            'classification_report': report
        }
    
    def print_results(self, metrics, class_names):
        """Print evaluation results"""
        print(f"\n{'='*60}")
        print("EVALUATION RESULTS")
        print(f"{'='*60}\n")
        
        print(f"Overall Accuracy: {metrics['accuracy']*100:.2f}%")
        print(f"Overall Precision: {metrics['precision']*100:.2f}%")
        print(f"Overall Recall: {metrics['recall']*100:.2f}%")
        print(f"Overall F1-Score: {metrics['f1_score']*100:.2f}%")
        
        print(f"\n{'-'*60}")
        print("Per-Class Metrics:")
        print(f"{'-'*60}")
        for i, class_name in enumerate(class_names):
            print(f"\n{class_name.upper()}:")
            print(f"  Precision: {metrics['precision_per_class'][i]*100:.2f}%")
            print(f"  Recall: {metrics['recall_per_class'][i]*100:.2f}%")
            print(f"  F1-Score: {metrics['f1_per_class'][i]*100:.2f}%")
        
        print(f"\n{'-'*60}")
        print("Confusion Matrix:")
        print(f"{'-'*60}")
        print(metrics['confusion_matrix'])
        print(f"\nRows: Actual | Columns: Predicted")
        
        print(f"\n{'-'*60}")
        print("Detailed Classification Report:")
        print(f"{'-'*60}")
        print(metrics['classification_report'])
        
        print(f"{'='*60}\n")
    
    def plot_confusion_matrix(self, cm, class_names, save_path='confusion_matrix.png'):
        """Plot and save confusion matrix"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names,
                   cbar_kws={'label': 'Count'})
        plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
        plt.ylabel('Actual Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to: {save_path}")
        plt.close()
    
    def evaluate_single_image(self, image_path):
        """Evaluate a single image"""
        from PIL import Image
        
        image = Image.open(image_path).convert('RGB')
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)
            prediction = torch.argmax(probabilities, dim=1).item()
        
        real_prob = probabilities[0][0].item()
        fake_prob = probabilities[0][1].item()
        
        return {
            'prediction': 'FAKE' if prediction == 1 else 'REAL',
            'confidence': max(real_prob, fake_prob) * 100,
            'real_probability': real_prob * 100,
            'fake_probability': fake_prob * 100
        }


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Evaluate Deepfake Detection Model')
    parser.add_argument('--model', type=str, default='deepfake_detector_best.pth',
                       help='Path to model checkpoint')
    parser.add_argument('--test_data', type=str, required=False,
                       help='Path to test dataset folder (should contain real/ and fake/ subfolders)')
    parser.add_argument('--image', type=str, required=False,
                       help='Path to single image for testing')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size for evaluation')
    
    args = parser.parse_args()
    
    # Initialize evaluator
    evaluator = ModelEvaluator(args.model)
    
    if args.test_data:
        # Evaluate on dataset
        evaluator.evaluate_on_dataset(args.test_data, args.batch_size)
    elif args.image:
        # Evaluate single image
        result = evaluator.evaluate_single_image(args.image)
        print(f"\n{'='*60}")
        print("SINGLE IMAGE PREDICTION")
        print(f"{'='*60}")
        print(f"Image: {args.image}")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.2f}%")
        print(f"Real Probability: {result['real_probability']:.2f}%")
        print(f"Fake Probability: {result['fake_probability']:.2f}%")
        print(f"{'='*60}\n")
    else:
        print("Please provide either --test_data or --image argument")
        print("\nExamples:")
        print("  python evaluate.py --test_data path/to/test_dataset")
        print("  python evaluate.py --image path/to/image.jpg")


if __name__ == "__main__":
    main()
