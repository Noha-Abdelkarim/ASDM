import os
import logging
import time
import random

from src.acd.acd_agent import ACDAgent
from src.sad.sad_agent import SADAgent
from src.dam.dam_agent import DAMAgent
from src.tsta.tsta_agent import TSTAAgent


# ---------- Logging Setup ----------
log_dir = "experiments/results_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "controller_C1.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("ControllerManager")


class ControllerManager:
    def __init__(self, controller_id="C1"):
        self.controller_id = controller_id

        logger.info(f"🚀 Initializing ControllerManager for {controller_id}")

        # Initialize all agents
        self.acd = ACDAgent(controller_id, "controller/config/controller_policy.json")
        logger.info("✅ ACD Agent initialized.")

        self.sad = SADAgent(controller_id)
        logger.info("✅ SAD Agent initialized.")

        self.dam = DAMAgent(controller_id)
        logger.info("✅ DAM Agent initialized.")

        self.tsta = TSTAAgent(controller_id)
        logger.info("✅ TSTA Agent initialized.")

        logger.info("🎯 ControllerManager initialization complete.")

    # -----------------------------------------------------
    def run(self):
        """
        Main event loop: collect telemetry → SAD detect → DAM mitigate
        + optional ACD/TSTA collaboration.
        """
        logger.info("🔄 ControllerManager running...")

        while True:
            features = self._get_dummy_features()

            # SAD Detection
            detected, attack_type = self.sad.detect(features)
            if detected:
                victim_ip = features.get("victim", "10.0.0.2")
                logger.info(f"🚨 Attack detected: {attack_type} on {victim_ip}")

                # Mitigation through DAM
                self.dam.mitigate(attack_type, victim_ip)

                # Collaboration through ACD
                self.acd.collaborate(attack_type, victim_ip)

                # Trust score adaptation through TSTA
                self.tsta.update_trust(attack_type, victim_ip)

            time.sleep(5)  # prevent tight loop

    # -----------------------------------------------------
    def _get_dummy_features(self):
        """
        Dummy telemetry generator for testing.
        Replace this with actual telemetry from Mininet/P4.
        """
        attacks = [
            {"protocol": "UDP", "dport": 80, "victim": "10.0.0.2"},
            {"protocol": "TCP", "flags": "S", "dport": 80, "victim": "10.0.0.2"},
            {"protocol": "ICMP", "victim": "10.0.0.2"},
            {"protocol": "HTTP", "dport": 80, "victim": "10.0.0.2"},
            {"protocol": "MIXED", "victim": "10.0.0.2"},
            {"protocol": "ARP", "victim": "10.0.0.2"},
        ]
        # randomly pick attack/no attack
        return random.choice(attacks + [{}])


# -----------------------------------------------------
if __name__ == "__main__":
    manager = ControllerManager(controller_id="C1")
    manager.run()
