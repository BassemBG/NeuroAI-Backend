from flask import Blueprint, request, jsonify
import torch
import numpy as np
from models.eeg_eog_model import load_model_and_scaler, preprocess_input

eeg_eog_bp = Blueprint('eeg_eog_bp', __name__)

model, scaler, device = load_model_and_scaler()

EMOTION_LABELS = ["anger", "sad", "fear", "neutral", "surprise", "happy", "disgust"]

@eeg_eog_bp.route('/predict', methods=['POST'])
def predict_emotion():
    data = request.get_json()

    if 'eye_features' not in data or 'eeg_features' not in data:
        return jsonify({'error': 'Missing eye_features or eeg_features'}), 400

    try:
        eye = np.array(data['eye_features'])       # shape: (W, E)
        eeg = np.array(data['eeg_features'])       # shape: (W, F, T)
        input_tensor = preprocess_input(eye, eeg, scaler).to(device)  # shape: (1, features, time)

        model.eval()
        with torch.no_grad():
            logits = model(input_tensor)
            predicted_class = int(torch.argmax(logits, dim=1).item())
            predicted_emotion = EMOTION_LABELS[predicted_class]

        return jsonify({'predicted_emotion': predicted_emotion})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
