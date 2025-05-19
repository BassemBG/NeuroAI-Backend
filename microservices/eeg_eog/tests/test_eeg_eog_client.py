import requests
import numpy as np
import scipy.io
from pathlib import Path

def test_api_eeg_eog():
    # Adjust this to point at your .mat files directory
    base_dir = Path(__file__).parent.parent / "models"
    eeg_mat = base_dir / "19 eeg_features.mat"
    eye_mat = base_dir / "19 eye_features.mat"

    # 1) Load .mat files
    mat_eeg = scipy.io.loadmat(str(eeg_mat))
    mat_eye = scipy.io.loadmat(str(eye_mat))

    # 2) Extract first non-meta variable from each
    eeg_array = next((v for k, v in mat_eeg.items() 
                      if not k.startswith("__")), None)
    eye_array = next((v for k, v in mat_eye.items() 
                      if not k.startswith("__")), None)

    # 3) Fallback to random if extraction failed
    if eeg_array is None or eye_array is None:
        print("⚠️  Could not extract from .mat → using random data")
        W = 100
        eeg_array = np.random.uniform(4, 36, size=(W, 17, 20))
        eye_array = np.random.uniform(5, 350, size=(W, 3))
    else:
        # maybe reshape or verify dims:
        print(f"Loaded EEG shape: {eeg_array.shape}")
        print(f"Loaded Eye shape: {eye_array.shape}")

    # 4) Limit/reshape to expected dims if needed
    W = min(100, eeg_array.shape[0], eye_array.shape[0])
    eeg_payload = eeg_array[:W].tolist()
    eye_payload = eye_array[:W].tolist()

    # 5) Send POST request
    url = "http://localhost:5004/api/eeg-eog/predict"
    payload = {
        "eye_features": eye_payload,
        "eeg_features": eeg_payload
    }
    print(f"→ Sending {W} windows of EEG and Eye to {url} ...")
    resp = requests.post(url, json=payload, headers={"Content-Type":"application/json"})

    # 6) Print results
    print("Status code:", resp.status_code)
    try:
        print("Response JSON:", resp.json())
    except ValueError:
        print("Response text:", resp.text)
        
        
def test_gateway_api_eeg_eog():
    # Adjust this to point at your .mat files directory
    base_dir = Path(__file__).parent.parent / "models"
    eeg_mat = base_dir / "1 eeg_features.mat"
    eye_mat = base_dir / "1 eye_features.mat"

    # 1) Load .mat files
    mat_eeg = scipy.io.loadmat(str(eeg_mat))
    mat_eye = scipy.io.loadmat(str(eye_mat))

    # 2) Extract first non-meta variable from each
    eeg_array = next((v for k, v in mat_eeg.items() 
                      if not k.startswith("__")), None)
    eye_array = next((v for k, v in mat_eye.items() 
                      if not k.startswith("__")), None)

    # 3) Fallback to random if extraction failed
    if eeg_array is None or eye_array is None:
        print("⚠️  Could not extract from .mat → using random data")
        W = 100
        eeg_array = np.random.uniform(4, 36, size=(W, 17, 20))
        eye_array = np.random.uniform(5, 350, size=(W, 3))
    else:
        # maybe reshape or verify dims:
        print(f"Loaded EEG shape: {eeg_array.shape}")
        print(f"Loaded Eye shape: {eye_array.shape}")

    # 4) Limit/reshape to expected dims if needed
    W = min(100, eeg_array.shape[0], eye_array.shape[0])
    eeg_payload = eeg_array[:W].tolist()
    eye_payload = eye_array[:W].tolist()

    # 5) Send POST request
    url = "http://localhost:7500/predict/eeg-eog"
    payload = {
        "eye_features": eye_payload,
        "eeg_features": eeg_payload
    }
    print(f"→ Sending {W} windows of EEG and Eye to {url} ...")
    resp = requests.post(url, json=payload, headers={"Content-Type":"application/json"})

    # 6) Print results
    print("Status code:", resp.status_code)
    try:
        print("Response JSON:", resp.json())
    except ValueError:
        print("Response text:", resp.text)


if __name__ == "__main__":
    test_api_eeg_eog()
    test_gateway_api_eeg_eog()
