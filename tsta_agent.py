import os
import logging

log_dir = "experiments/results_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "tsta_C1.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("TSTAAgent")


class TSTAAgent:
    def __init__(self, controller_id):
        self.controller_id = controller_id
        self.trust_scores = {}  # victim_ip → trust_score
        logger.info(f"✅ TSTA Agent initialized for controller {controller_id}")

    def update_trust(self, attack_type, victim_ip):
        """
        Adjust trust scores based on attack detection.
        """
        old_score = self.trust_scores.get(victim_ip, 1.0)

        # Simple decay model
        new_score = max(0.0, old_score - 0.1)
        self.trust_scores[victim_ip] = new_score

        logger.info(f"[TSTA] 🔄 Trust score updated for {victim_ip}: {old_score:.2f} → {new_score:.2f} due to {attack_type}")
        print(f"[TSTA] 🔄 Trust for {victim_ip}: {new_score:.2f}")
        return new_score

    def get_trust(self, victim_ip):
        """Retrieve trust score for victim_ip"""
        return self.trust_scores.get(victim_ip, 1.0)
