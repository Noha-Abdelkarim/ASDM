import os
import logging
from datetime import datetime

log_dir = "experiments/results_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "sad_C1.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("SADAgent")


class SADAgent:
    def __init__(self, controller_id, model_path=None, scaler_path=None):
        self.controller_id = controller_id
        logger.info(f"✅ SAD Agent initialized for controller {controller_id}")

    def detect(self, features):
        """
        Dummy detection logic – replace with ML model inference later.
        Here we just classify based on protocol/flags/ports.
        """
        try:
            protocol = features.get("protocol", "")
            dport = features.get("dport", 0)
            flags = features.get("flags", "")

            attack_type = None
            if protocol == "UDP":
                attack_type = "UDP Flood"
            elif protocol == "TCP" and flags == "S":
                attack_type = "TCP SYN Flood"
            elif protocol == "ICMP":
                attack_type = "ICMP Flood"
            elif protocol == "HTTP":
                attack_type = "HTTP Flood"
            elif protocol == "MIXED":
                attack_type = "Mixed Flood"
            else:
                attack_type = "Unknown/Other"

            logger.info(f"[DETECTED] 🚨 DDoS Attack Detected: {attack_type}")
            return True, attack_type

        except Exception as e:
            logger.error(f"SAD detection error: {e}")
            return False, None
