import requests
import os

def test_speech_emotion():
    url = "http://localhost:5000/api/speech/predict"
    audio_path = "tests/test_input_data/short_audio_data/neutral.wav"  # Path to a short 2.5s test audio file

    if not os.path.exists(audio_path):
        print(f"File {audio_path} not found.")
        return

    with open(audio_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, files=files)
        print("Single audio prediction:", response.json())


def test_docker_container_speech_emotion():
    url = "http://localhost:5002/api/speech/predict"
    audio_path = "tests/test_input_data/short_audio_data/surprise.wav"  # Path to a short 2.5s test audio file

    if not os.path.exists(audio_path):
        print(f"File {audio_path} not found.")
        return

    with open(audio_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, files=files)
        print("Single audio prediction:", response.json())

def test_docker_gateway_container_speech_emotion():
    url = "http://localhost:7500/predict/speech"
    audio_path = "tests/test_input_data/short_audio_data/surprise.wav"  # Path to a short 2.5s test audio file

    if not os.path.exists(audio_path):
        print(f"File {audio_path} not found.")
        return

    with open(audio_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, files=files)
        print("Single audio prediction:", response.json())


def test_sliding_window_speech_emotion():
    url = "http://localhost:5000/api/speech/predict_sliding"
    audio_path = "tests/test_input_data/sliding_window_data/hap.wav"  # Path to a longer test audio file (e.g. ~10s)

    if not os.path.exists(audio_path):
        print(f"File {audio_path} not found.")
        return

    with open(audio_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, files=files)
        print("Sliding window prediction:", response.json())

if __name__ == "__main__":
    #test_speech_emotion()
    test_docker_container_speech_emotion()
    #test_sliding_window_speech_emotion()
    test_docker_gateway_container_speech_emotion()