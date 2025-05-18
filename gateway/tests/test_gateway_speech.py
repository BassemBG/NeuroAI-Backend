import requests
import os

def test_speech_emotion():
    url = "http://localhost:7085/predict/speech"
    audio_path = "tests/test_input_data/short_audio_data/neutral.wav"  # Path to a short 2.5s test audio file

    if not os.path.exists(audio_path):
        print(f"File {audio_path} not found.")
        return

    with open(audio_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, files=files)
        print("Single audio prediction:", response.json())
        
if __name__ == "__main__":
    test_speech_emotion()
