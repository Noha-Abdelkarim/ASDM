"""
ASDM - Metrics Utility
----------------------
Provides basic evaluation metrics for detection & mitigation.
"""

import numpy as np


def detection_rate(tp: int, fn: int) -> float:
    """True Positive Rate = TP / (TP + FN)."""
    return tp / (tp + fn + 1e-9)


def false_alarm_rate(fp: int, tn: int) -> float:
    """False Alarm Rate = FP / (FP + TN)."""
    return fp / (fp + tn + 1e-9)


def mitigation_latency(detection_time: float, mitigation_time: float) -> float:
    """Calculate latency between detection and mitigation."""
    return mitigation_time - detection_time


def recovery_score(latencies: list) -> float:
    """Average recovery time after mitigation actions."""
    return float(np.mean(latencies)) if latencies else 0.0
