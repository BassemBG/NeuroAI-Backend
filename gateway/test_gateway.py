# test_gateway.py
import requests


def test_facial_emotion():
    url = "http://localhost:7085/api/facial/predict"
    image_path = "../microservices/Facial_emotion_microservice/tests/image0000311.jpg"

    with open(image_path, "rb") as img:
        files = {"image": img}
        response = requests.post(url, files=files)

    print("Status:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    test_facial_emotion()

