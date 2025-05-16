from flask import Flask, request, jsonify

import requests

app = Flask(__name__)

@app.route("/predict/speech", methods=["GET"])
def predict_speech():
    #audio = request.files['file']
    print("Received request for speech emotion prediction")
    response = requests.get("http://speech_emotion_microservice:5000/predict")
    return jsonify(response.json())

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
