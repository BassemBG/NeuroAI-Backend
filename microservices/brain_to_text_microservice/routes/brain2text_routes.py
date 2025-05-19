from flask import Blueprint, request, jsonify
import scipy.io
import tempfile
import os
from models.brain_model import predict_from_mat

brain_to_text_blueprint = Blueprint('brain_to_text', __name__)

@brain_to_text_blueprint.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No .mat file provided'}), 400

    file = request.files['file']

    try:
        with tempfile.NamedTemporaryFile(suffix='.mat', delete=False) as tmp:
            temp_path = tmp.name
            file.save(temp_path)

        mat = scipy.io.loadmat(temp_path)

        os.remove(temp_path)

        predictions = predict_from_mat(mat)
        return jsonify({'predictions': predictions})

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print("Prediction error:", e)
        return jsonify({'error': str(e)}), 500
