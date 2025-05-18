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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7085)
