import os
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

# ---- Ensure models directory exists ----
model_dir = "src/sad/models"
os.makedirs(model_dir, exist_ok=True)

# ---- Create a dummy scaler ----
# Fit it on some fake data just so it has mean/std
X_dummy = np.random.rand(100, 3) * 100  # 100 samples, 3 features
scaler = StandardScaler()
scaler.fit(X_dummy)

# ---- Save scaler ----
scaler_path = os.path.join(model_dir, "scaler.pkl")
joblib.dump(scaler, scaler_path)

print(f"✅ Dummy scaler saved at {scaler_path}")
