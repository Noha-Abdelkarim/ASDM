"""
ASDM - Evaluation Script
------------------------
Analyzes logs from experiments and reports detection & mitigation results.
"""

import os

def evaluate_results(log_dir="experiments/results_logs/"):
    results = {
        "detections": [],
        "mitigations": []
    }

    detection_log = os.path.join(log_dir, "sad.log")
    mitigation_log = os.path.join(log_dir, "dam.log")

    if os.path.exists(detection_log):
        with open(detection_log, "r") as f:
            results["detections"] = f.readlines()

    if os.path.exists(mitigation_log):
        with open(mitigation_log, "r") as f:
            results["mitigations"] = f.readlines()

    return results


if __name__ == "__main__":
    res = evaluate_results()
    print("=== Evaluation Report ===")
    print("Detections:", len(res["detections"]))
    print("Mitigations:", len(res["mitigations"]))

