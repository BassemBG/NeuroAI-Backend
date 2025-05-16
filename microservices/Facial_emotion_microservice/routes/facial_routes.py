from flask import Blueprint, request, jsonify
from models.facial_emotion_model import FacialEmotionModel

facial_bp = Blueprint('facial', __name__)
model = FacialEmotionModel()

@facial_bp.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image_file = request.files['image']
        image_bytes = image_file.read()
        predicted_emotion = model.predict(image_bytes)

        return jsonify({
            'emotion': predicted_emotion,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500