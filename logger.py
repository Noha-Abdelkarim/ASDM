"""
ASDM - Central Logger Utility
-----------------------------
Provides a consistent logging setup across modules.
"""

import logging
import os


def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    Create and return a logger.
    """
    os.makedirs("experiments/results_logs", exist_ok=True)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
