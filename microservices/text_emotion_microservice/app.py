from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def predict():
    #text = request.json.get("text")
    # Dummy prediction
    return jsonify({"emotion": "neutral"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)