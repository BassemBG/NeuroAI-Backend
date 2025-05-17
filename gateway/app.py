from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
