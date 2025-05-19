import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from models.speech_emotion_model import SpeechEmotionModel

speech_bp = Blueprint('speech_bp', __name__)
speech_model = SpeechEmotionModel()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 1. For standard 2.5s audio
@speech_bp.route('/predict', methods=['POST'])
def predict_speech_emotion():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    print(f"[INFO] Saving uploaded file to {filepath}")

    try:
        file.save(filepath)
        print(f"[INFO] File saved. Now calling model on {filepath}")

        emotion = speech_model.predict(filepath)
        print(f"[INFO] Model prediction: {emotion}")

        return jsonify({'emotion': emotion})
    except Exception as e:
        import traceback
        traceback.print_exc()  # Will show full traceback in Docker logs
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"[INFO] File {filepath} deleted after prediction")


# 2. For long audio with sliding window
@speech_bp.route('/predict_sliding', methods=['POST'])
def predict_speech_emotion_sliding():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename) 
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        results = speech_model.predict_sliding_window(filepath)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
