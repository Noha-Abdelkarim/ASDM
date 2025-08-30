import os
import logging
import json

log_dir = "experiments/results_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "acd_C1.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("ACDAgent")


class ACDAgent:
    def __init__(self, controller_id, policy_file="controller/config/controller_policy.json"):
        self.controller_id = controller_id
        self.policy_file = policy_file
        self.policy = self.load_policy()
        logger.info(f"✅ ACD Agent initialized for controller {controller_id}")

    def load_policy(self):
        """Load collaboration policy (if exists)"""
        if os.path.exists(self.policy_file):
            try:
                with open(self.policy_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"❌ Failed to load ACD policy: {e}")
        logger.warning(f"⚠️ ACD policy file not found at {self.policy_file}, using defaults.")
        return {"collaboration_enabled": True}

    def collaborate(self, attack_type, victim_ip):
        """
        Share attack context with peers.
        """
        if not self.policy.get("collaboration_enabled", True):
            logger.info(f"[ACD] 🚫 Collaboration disabled. Skipping.")
            return False

        logger.info(f"[ACD] 🤝 Sharing anomaly context with peers: {attack_type} at {victim_ip}")
        print(f"[ACD] 🤝 Shared anomaly info → {attack_type} targeting {victim_ip}")
        return True
