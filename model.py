import torch
import torch.nn as nn
import torchvision.models as models

class DeepfakeDetector(nn.Module):
    """
    Deepfake Detection Model based on ResNet50 architecture
    Modify this if your model uses a different architecture
    """
    def __init__(self, num_classes=2):
        super(DeepfakeDetector, self).__init__()
        # Using ResNet50 as backbone
        self.model = models.resnet50(pretrained=False)
        
        # Modify the final fully connected layer
        num_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        return self.model(x)


class DeepfakeDetectorEfficientNet(nn.Module):
    """
    Alternative model using EfficientNet
    Use this if your model was trained with EfficientNet
    """
    def __init__(self, num_classes=2):
        super(DeepfakeDetectorEfficientNet, self).__init__()
        try:
            from efficientnet_pytorch import EfficientNet
            self.model = EfficientNet.from_name('efficientnet-b0')
            num_features = self.model._fc.in_features
            self.model._fc = nn.Sequential(
                nn.Linear(num_features, 512),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(512, num_classes)
            )
        except ImportError:
            print("EfficientNet not available, using ResNet50 instead")
            self.model = models.resnet50(pretrained=False)
            num_features = self.model.fc.in_features
            self.model.fc = nn.Sequential(
                nn.Linear(num_features, 512),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(512, num_classes)
            )
    
    def forward(self, x):
        return self.model(x)


class SimpleDeepfakeDetector(nn.Module):
    """
    Simple CNN model for deepfake detection
    Use this if your model uses a custom simple architecture
    """
    def __init__(self, num_classes=2):
        super(SimpleDeepfakeDetector, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


class CNNLSTMDeepfakeDetector(nn.Module):
    """
    CNN + LSTM model for deepfake detection (for video/sequence analysis)
    This matches the architecture in your trained model
    """
    def __init__(self, num_classes=1, hidden_size=256, num_layers=2):
        super(CNNLSTMDeepfakeDetector, self).__init__()
        
        # CNN for feature extraction (matches your model: 32 -> 64 -> 128)
        self.cnn = nn.Module()
        self.cnn.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 32 channels
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),  # 64 channels
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),  # 128 channels
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )
        # Input: 224x224, after 3 poolings (2x each): 224/8 = 28x28
        # So 128 * 28 * 28 = 100352, but your model has 32768
        # This means input might be 128x128: 128/8 = 16, so 128*16*16 = 32768
        self.cnn.fc = nn.Sequential(
            nn.Linear(32768, 512)  # Matches your model
        )
        
        # LSTM for temporal analysis
        self.lstm = nn.LSTM(
            input_size=512,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True
        )
        
        # Classifier (output is 1 for binary classification with sigmoid)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size * 2, 128),  # *2 for bidirectional
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)  # 1 output class
        )
    
    def forward(self, x):
        batch_size = x.size(0)
        
        # CNN feature extraction
        x = self.cnn.features(x)
        x = x.view(batch_size, -1)
        x = self.cnn.fc(x)
        
        # LSTM (reshape for sequence)
        x = x.unsqueeze(1)  # Add sequence dimension
        x, _ = self.lstm(x)
        x = x[:, -1, :]  # Take last output
        
        # Classification
        x = self.classifier(x)
        return x
