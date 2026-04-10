"""
ASDM - Dataset Loader
---------------------
Utility to load benchmark datasets for training/testing:
 - CIC-IoMT 2024
 - UNSW-NB15
 - ToN-IoT
 - CIC-IoT 2023
"""

import pandas as pd
import os


class DatasetLoader:
    def __init__(self, base_path="datasets/"):
        self.base_path = base_path

    def load_csv(self, dataset_name: str, file_name: str) -> pd.DataFrame:
        """
        Load dataset CSV file into Pandas DataFrame.
        """
        path = os.path.join(self.base_path, dataset_name, file_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset file not found: {path}")
        return pd.read_csv(path)

    def load_all(self) -> dict:
        """
        Load references to available datasets.
        """
        datasets = {
            "CIC-IoMT-2024": os.path.join(self.base_path, "CIC-IoMT-2024"),
            "UNSW-NB15": os.path.join(self.base_path, "UNSW-NB15"),
            "ToN_IoT": os.path.join(self.base_path, "ToN_IoT"),
            "CIC-IoT-2023": os.path.join(self.base_path, "CIC-IoT-2023"),
        }
        return datasets
