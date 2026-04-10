"""
ASDM - Experiment Runner
------------------------
Executes end-to-end experiments:
 - Deploys topology
 - Starts controller pipeline
 - Launches attack traffic
 - Collects detection & mitigation results
"""

import logging
import time
from controller.controller_manager import ControllerManager
from attack_simulator.attack_launcher import AttackLauncher

def run_experiment():
    logging.basicConfig(
        filename="experiments/results_logs/experiment.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("=== Starting ASDM Experiment ===")

    # Initialize controller
    controller = ControllerManager(controller_id="C1")

    # Initialize attacker
    attacker = AttackLauncher(target_ip="10.0.0.2", target_port=80)

    # Benign traffic simulation (placeholder)
    benign_packets = [
        {"src_ip": "10.0.0.1", "dst_ip": "10.0.0.2", "size": 400, "proto": "TCP", "timestamp": time.time()},
        {"src_ip": "10.0.0.3", "dst_ip": "10.0.0.4", "size": 500, "proto": "UDP", "timestamp": time.time()},
    ]
    for pkt in benign_packets:
        controller.process_packet(pkt)

    # Launch attack traffic
    attacker.syn_flood(count=50)
    attacker.udp_flood(count=20)

    logging.info("=== Experiment Completed ===")


if __name__ == "__main__":
    run_experiment()
