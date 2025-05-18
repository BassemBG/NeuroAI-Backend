from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL of the facial emotion microservice
FACIAL_MICROSERVICE_URL = "http://facial_emotion_microservice:5001/api/facial/predict"




@app.route("/api/facial/predict", methods=["POST"])
def predict_facial():
    if "image" not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    image = request.files["image"]
    files = {
        "image": (image.filename, image.stream, image.mimetype)
    }

    try:
        response = requests.post(FACIAL_MICROSERVICE_URL, files=files)

        if response.status_code != 200:
            return jsonify({
                "error": f"Facial microservice returned status code {response.status_code}",
                "details": response.text
            }), response.status_code

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"Gateway level error": str(e)}), 500

@app.route("/predict/speech", methods=["POST"])
def predict_speech():
    if "file" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    file = request.files["file"]
    files = {"file": (file.filename, file.stream, file.mimetype)}

    try:
        response = requests.post("http://speech_emotion_microservice:5000/api/speech/predict", files=files)
        
        if response.status_code != 200:
            return jsonify({"error": f"Speech microservice returned status code {response.status_code}", "details": response.text}), response.status_code

        print("Response from speech emotion microservice:", response.json())
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"Gateway level error": str(e)}), 500


#hejer
@app.route("/predict/eeg-eog", methods=["POST"])
def predict_eeg_eog():
    response = requests.post("http://eeg_eog:5000/predict", json=request.get_json())
    return jsonify(response.json())

@app.route("/predict/eeg-keypress", methods=["POST"])
def predict_eeg_keypress():
    try:
        # Forward the incoming request's JSON to the microservice
        response = requests.post(
            "http://eeg_keypress_microservice:5005/predict", 
            json=request.get_json()
        )
        
        # Forward status and response
        return (response.content, response.status_code, response.headers.items())

    except requests.exceptions.RequestException as e:
        print("Proxying eeg-keypress request to microservice failed. Exception:", e)
        return jsonify({"error": "Failed to connect to microservice", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7085)
