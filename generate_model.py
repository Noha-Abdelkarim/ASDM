import tensorflow as tf

# Define a small LSTM+GRU model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(10, 5)),   # Example input: 10 timesteps, 5 features
    tf.keras.layers.LSTM(16, return_sequences=True),
    tf.keras.layers.GRU(8),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

# Compile (required before saving)
model.compile(optimizer="adam", loss="binary_crossentropy")

# Save to the expected path
model.save("src/sad/models/lstm_gru_model.h5")

print("✅ Dummy model generated at src/sad/models/lstm_gru_model.h5")
