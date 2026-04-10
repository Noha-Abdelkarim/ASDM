"""
ASDM - SAD Preprocessing
------------------------
Feature normalization & transformation pipeline for SAD.
"""

import numpy as np


class Preprocessor:
    def transform(self, features: dict, scaler) -> np.ndarray:
        """
        Transform feature dict into scaled array for inference.
        """
        keys = sorted(features.keys())  # Consistent feature order
        values = np.array([features[k] for k in keys]).reshape(1, -1)
        scaled = scaler.transform(values)
        return scaled
