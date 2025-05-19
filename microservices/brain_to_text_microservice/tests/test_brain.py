import unittest
import requests

class TestBrainModel(unittest.TestCase):
    def test_prediction(self):
        with open('tests/test/t12.2022.04.28.mat', 'rb') as f:
            response = requests.post("http://localhost:5000/predict", files={'file': f})

        # Assert that the request was successful
        self.assertEqual(response.status_code, 200)

        # Optional: Check that expected keys exist in JSON response
        data = response.json()
        print("Response JSON:", data)  # Helpful for debugging



if __name__ == '__main__':
    unittest.main()
