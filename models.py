"""
ASDM - LSTM-GRU Hybrid Model
----------------------------
Defines the deep learning architecture for sequential anomaly detection.
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout


def build_lstm_gru_model(input_shape, learning_rate=0.001):
    """
    Build a hybrid LSTM-GRU model for anomaly detection.
    :param input_shape: tuple (timesteps, features)
    """
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    model.add(GRU(64))
    model.add(Dropout(0.3))
    model.add(Dense(1, activation="sigmoid"))

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss="binary_crossentropy", metrics=["accuracy"])
    return model
