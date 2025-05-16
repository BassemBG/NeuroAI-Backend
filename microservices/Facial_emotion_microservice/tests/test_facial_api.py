import requests
import os

def test_facial_emotion():
    url = "http://localhost:5000/api/facial/predict"
    image_path = "image0000311.jpg"  # Update path as needed

    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        response = requests.post(url, files=files)
        print(response.json())

if __name__ == "__main__":
    test_facial_emotion()