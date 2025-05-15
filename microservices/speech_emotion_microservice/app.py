from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def predict():
    # Dummy inference for demonstration
    return jsonify({"emotion": "happy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)