"""
ASDM - SAD Training Script
--------------------------
Trains the LSTM-GRU hybrid on IoT/SDN datasets (CIC-IoMT 2024, UNSW-NB15, ToN-IoT, CIC-IoT-2023).
"""

import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping
from .models import build_lstm_gru_model
from .preprocess import Preprocessor


def train_sad(X_train, y_train, X_val, y_val, save_model_path="src/sad/models/lstm_gru_model.h5",
              save_scaler_path="src/sad/models/scaler.pkl"):
    """
    Train the SAD hybrid model and save it.
    """
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)

    # Reshape for sequential model
    X_train = np.expand_dims(X_train, axis=1)
    X_val = np.expand_dims(X_val, axis=1)

    model = build_lstm_gru_model(input_shape=(1, X_train.shape[2]))

    es = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=64,
        callbacks=[es]
    )

    # Save artifacts
    model.save(save_model_path)
    joblib.dump(scaler, save_scaler_path)
    print(f"Model saved at {save_model_path}, Scaler saved at {save_scaler_path}")
