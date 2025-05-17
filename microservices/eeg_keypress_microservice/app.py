from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import pickle

app = Flask(__name__)

# Load model and label encoder
model = load_model("models/best_LSTM.keras")
with open("models/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if "features" not in data:
        return jsonify({"error": "Missing 'features' key in JSON payload. Expected format: { 'features': [float, ..., float] }"}), 400

    if len(data["features"]) != 69:
        return jsonify({"error": f"Expected 69 features, but got {len(data['features'])}"}), 400

    try:
        features = np.array(data["features"], dtype=np.float32).reshape(1, 1, 69)  
        prediction = model.predict(features)
        predicted_index = int(np.argmax(prediction))
        predicted_label = label_encoder.inverse_transform([predicted_index])[0]

        return jsonify({
            "predicted_index": predicted_index,
            "predicted_label": predicted_label
        })
    except Exception as e:
        return jsonify({"error": "Model prediction failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
