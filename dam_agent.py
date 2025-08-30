import os
import logging
import json

log_dir = "experiments/results_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "dam_C1.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("DAMAgent")


class DAMAgent:
    def __init__(self, controller_id, policy_file="controller/config/block_policy.json"):
        self.controller_id = controller_id
        self.policy_file = policy_file
        self.policy = self.load_policy()
        logger.info(f"✅ DAM Agent initialized for controller {controller_id}")

    def load_policy(self):
        """Load mitigation policies from JSON file if available"""
        if os.path.exists(self.policy_file):
            try:
                with open(self.policy_file, "r") as f:
                    policy = json.load(f)
                    logger.info(f"✅ Loaded DAM policy from {self.policy_file}")
                    return policy
            except Exception as e:
                logger.error(f"❌ Failed to load policy: {e}")
        logger.warning(f"⚠️ Policy file not found at {self.policy_file}. Using defaults.")
        return {}

    def mitigate(self, attack_type, victim_ip):
        """
        Apply mitigation based on attack type.
        Logs actions; in a real P4/SDN setup this would push rules.
        """
        try:
            action = None

            if attack_type == "UDP Flood":
                action = f"Rate-limit UDP traffic towards {victim_ip}"
            elif attack_type == "TCP SYN Flood":
                action = f"Install SYN cookies / drop excessive SYNs for {victim_ip}"
            elif attack_type == "ICMP Flood":
                action = f"Block ICMP echo requests to {victim_ip}"
            elif attack_type == "HTTP Flood":
                action = f"Throttle HTTP requests / blacklist offender for {victim_ip}"
            elif attack_type == "Mixed Flood":
                action = f"Apply composite rules: drop UDP + rate-limit TCP for {victim_ip}"
            elif attack_type == "ARP Spoof":
                action = f"Block forged ARP replies targeting {victim_ip}"
            else:
                action = f"No predefined mitigation. Monitor traffic to {victim_ip}"

            logger.info(f"[MITIGATION] 🚫 {attack_type} detected → {action}")
            print(f"[DAM] 🚫 {attack_type} → {action}")

            return True, action

        except Exception as e:
            logger.error(f"DAM mitigation error: {e}")
            return False, None
