""" import requests
import numpy as np

# 20 features
features = np.random.rand(69).tolist()

response = requests.post(
    "http://127.0.0.1:7000/predict",
    json={"features": features}
)

print(response.json())
 """
 
import requests

url = "http://127.0.0.1:7500/predict/eeg-keypress"
data = {
    "features": [0.1] * 69  # Example dummy input, replace with your actual data
}

response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Response content:", response.text)  # raw content

try:
    print("JSON response:", response.json())
except Exception as e:
    print("Failed to decode JSON:", e)
