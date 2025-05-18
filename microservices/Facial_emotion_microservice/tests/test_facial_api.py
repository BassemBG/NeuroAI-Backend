# import requests
# import os

# def test_facial_emotion():
#     url = "http://localhost:5000/api/facial/predict"
#     image_path = "image0000311.jpg"  # Update path as needed

#     with open(image_path, "rb") as image_file:
#         files = {"image": image_file}
#         response = requests.post(url, files=files)
#         print(response.json())

# if __name__ == "__main__":
#     test_facial_emotion()


from flask import Flask, request, jsonify
from models.facial_emotion_model import FacialEmotionModel

app = Flask(__name__)
model = FacialEmotionModel()


@app.route('/predict', methods=['POST'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
