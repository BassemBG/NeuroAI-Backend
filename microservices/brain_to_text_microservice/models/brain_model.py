import numpy as np
import json
import scipy.io
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json

# Load model and tokenizer once
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'lstm_model.h5')
TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), 'tokenizer.json')

model = load_model(MODEL_PATH)

with open(TOKENIZER_PATH) as f:
    tokenizer = tokenizer_from_json(json.load(f))

area6v_indices = np.arange(0, 128)
max_timesteps = 906    # fixed input length for model
max_label_len = 88     # fixed output length for model

def preprocess_trial(mat_data):
    spikePow = mat_data['spikePow'].squeeze()
    tx1 = mat_data['tx1'].squeeze()
    blockIdx = mat_data['blockIdx'].squeeze()
    sentenceText = mat_data['sentenceText']

    num_trials = len(spikePow)
    X_preprocessed = []
    y_texts = []

    for i in range(num_trials):
        spike_trial = spikePow[i][:, area6v_indices]
        tx1_trial = tx1[i][:, area6v_indices]
        trial_features = np.concatenate([spike_trial, tx1_trial], axis=1)

        block_id = blockIdx[i]
        block_mask = (blockIdx == block_id)
        block_trials = [np.concatenate([spikePow[j][:, area6v_indices], tx1[j][:, area6v_indices]], axis=1)
                        for j in range(num_trials) if block_mask[j]]
        block_data = np.vstack(block_trials)
        mean = block_data.mean(axis=0)
        std = block_data.std(axis=0) + 1e-8

        trial_features = (trial_features - mean) / std
        X_preprocessed.append(trial_features)

        # Decode sentence text from mat
        sentence_entry = sentenceText[i]
        if isinstance(sentence_entry, np.ndarray):
            sentence = ''.join(chr(int(c)) for c in sentence_entry.flatten() if c != 0)
        elif isinstance(sentence_entry, str):
            sentence = sentence_entry
        else:
            sentence = str(sentence_entry)
        y_texts.append(sentence)

    return X_preprocessed, y_texts

def decode_output(predicted_sequence):
    index_word = {v: k for k, v in tokenizer.word_index.items()}
    decoded = []
    for token_id in predicted_sequence:
        if token_id == 0:
            continue
        word = index_word.get(token_id, '')
        decoded.append(word)
    return ' '.join(decoded)

def predict_from_mat(mat):
    X_input, y_texts = preprocess_trial(mat)

    # Pad inputs for model (X padded on time dimension, features fixed)
    X_padded = np.array([
        np.pad(x[:max_timesteps], ((0, max(0, max_timesteps - x.shape[0])), (0, 0)), mode='constant')
        for x in X_input
    ], dtype='float32')

    # Tokenize and pad the target texts to feed as second input
    y_sequences = tokenizer.texts_to_sequences(y_texts)
    y_padded = pad_sequences(y_sequences, maxlen=max_label_len, padding='post')

    # Predict using model: **two inputs expected**
    y_pred = model.predict([X_padded, y_padded])

    predicted_sentences = []
    for pred in y_pred:
        token_ids = np.argmax(pred, axis=1)
        sentence = decode_output(token_ids)
        predicted_sentences.append(sentence)
    return predicted_sentences
