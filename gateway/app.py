from flask import Flask, request, jsonify

import requests

app = Flask(__name__)

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


@app.route("/predict/text", methods=["GET"])
def predict_text():
    print("Received request for text emotion prediction")
    #text = request.json.get("text")
    response = requests.get("http://text_emotion_microservice:4000/predict")
    print(response)
    return jsonify(response.json())
#hejer
@app.route("/predict/eeg-eog", methods=["POST"])
def predict_eeg_eog():
    response = requests.post("http://eeg_eog:5000/predict", json=request.get_json())
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7085)
