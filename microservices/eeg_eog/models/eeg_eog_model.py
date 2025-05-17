import torch
import torch.nn as nn
import torch.nn.functional as F
import joblib
import numpy as np

class CNN1DClassifier(nn.Module):
    def __init__(self, n_feats, n_classes):
        super().__init__()
        self.conv1 = nn.Conv1d(n_feats, 64, 3, padding=1)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(64, 128, 3, padding=1)
        self.pool2 = nn.MaxPool1d(2)
        self.global_pool = nn.AdaptiveAvgPool1d(1)
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(128, n_classes)

    def forward(self, x):
        x = F.relu(self.conv1(x)); x = self.pool1(x)
        x = F.relu(self.conv2(x)); x = self.pool2(x)
        x = self.global_pool(x).squeeze(-1)
        x = self.dropout(x)
        return self.fc(x)

def load_model_and_scaler():
    scaler = joblib.load("models/robust_scaler.pkl")
    model = CNN1DClassifier(n_feats=343, n_classes=7)
    model.load_state_dict(torch.load("models/model.pt", map_location=torch.device('cpu')))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return model, scaler, device

def preprocess_input(eye_arr, eeg_arr, scaler):
    # Flatten EEG: (W, F, T) → (W, F*T)
    eeg_flat = eeg_arr.reshape(eeg_arr.shape[0], -1)
    combined = np.hstack([eye_arr, eeg_flat])  # (W, E+F*T)
    
    # Log1p + Scale
    min_val = combined.min()
    shift = -min_val + 1e-6 if min_val < 0 else 0.0
    log_combined = np.log1p(combined + shift)
    scaled = scaler.transform(log_combined)

    # Convert to torch tensor: (features, time)
    tensor = torch.tensor(scaled.T, dtype=torch.float32).unsqueeze(0)  # (1, features, time)
    return tensor
