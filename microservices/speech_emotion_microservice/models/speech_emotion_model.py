import numpy as np
import librosa
import pickle

from tensorflow.keras.models import model_from_json

class SpeechEmotionModel:
    def __init__(self):
        # Load model
        with open("models/CNN_model.json", 'r') as json_file:
            loaded_model_json = json_file.read()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights("models/CNN_model_weights.h5")

        # Load scaler and encoder
        with open('models/scaler2.pickle', 'rb') as f:
            self.scaler = pickle.load(f)

        with open('models/encoder2.pickle', 'rb') as f:
            self.encoder = pickle.load(f)

    def _zcr(self, data, frame_length=2048, hop_length=512):
        return np.squeeze(librosa.feature.zero_crossing_rate(data, frame_length=frame_length, hop_length=hop_length))

    def _rmse(self, data, frame_length=2048, hop_length=512):
        return np.squeeze(librosa.feature.rms(y=data, frame_length=frame_length, hop_length=hop_length))

    def _mfcc(self, data, sr, flatten=True):
        mfcc = librosa.feature.mfcc(y=data, sr=sr)
        return np.ravel(mfcc.T) if flatten else np.squeeze(mfcc.T)

    def extract_features(self, data, sr):
        zcr = self._zcr(data)
        rmse = self._rmse(data)
        mfcc = self._mfcc(data, sr)
        features = np.hstack([zcr, rmse, mfcc])
        return features

    def preprocess(self, path):
        data, sr = librosa.load(path, duration=2.5, offset=0.6)
        features = self.extract_features(data, sr)
        scaled = self.scaler.transform([features])
        final = np.expand_dims(scaled, axis=2)
        return final

    def predict(self, path):
        input_data = self.preprocess(path)
        predictions = self.model.predict(input_data)
        emotion = self.encoder.inverse_transform(predictions)[0][0]
        return emotion

    def predict_sliding_window(self, path, chunk_duration=2.5, step=2.5):
        audio, sr = librosa.load(path, sr=None)
        total_duration = librosa.get_duration(y=audio, sr=sr)
        
        print(f"Total audio duration: {total_duration}s")
        print(f"Expected chunks from 0 to {total_duration - chunk_duration} by {step}")


        
        predictions = []
        for start in np.arange(0, total_duration - chunk_duration + 0.01, step):
            end = start + chunk_duration
            chunk = audio[int(sr * start):int(sr * end)]
            
            if len(chunk) < int(sr * chunk_duration):  # Pad if too short
                chunk = np.pad(chunk, (0, int(sr * chunk_duration) - len(chunk)))

            target_feature_length = 2376
            features = self.extract_features(chunk, sr)
            if len(features) < target_feature_length:
                features = np.pad(features, (0, target_feature_length - len(features)))
            elif len(features) > target_feature_length:
                features = features[:target_feature_length]

            scaled = self.scaler.transform([features])
            print("scaled:", scaled)

            final = np.expand_dims(scaled, axis=2)
            print("final shape:", final.shape)
            pred = self.model.predict(final)
            decoded = self.encoder.inverse_transform(pred)[0][0]
            print("debugging display, decoded:", decoded)
            predictions.append(decoded)

        # Majority vote
        if predictions:
            final_prediction = max(set(predictions), key=predictions.count)
        else:
            print("No predictions are made.")
            final_prediction = "Unknown"

        return {
            "prediction": final_prediction,
            "all_chunk_predictions": predictions
        }
