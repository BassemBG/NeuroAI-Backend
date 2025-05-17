import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
import pickle

class EegEmotionModel:
    def __init__(self):
        # Load trained Keras model
        self.model = load_model("modelS/best_LSTM.h5")
        
        # Load LabelEncoder if saved, or define manually
        with open("models/label_encoder.pkl", "rb") as f:
            self.label_encoder = pickle.load(f)

    def preprocess(self, features):
        """
        Preprocess input features into model-ready format.
        :param features: List or array of EEG features
        :return: reshaped numpy array
        """
        X = np.array(features, dtype=np.float32).reshape(1, 1, -1)  # shape: (1 sample, 1 timestep, n_features)
        return X

    def predict(self, features):
        """
        Predict emotion from input features
        :param features: List of EEG features
        :return: Emotion label
        """
        X = self.preprocess(features)
        y_prob = self.model.predict(X)
        y_pred = np.argmax(y_prob, axis=1)[0]
        predicted_emotion = self.label_encoder.inverse_transform([y_pred])[0]
        return predicted_emotion
