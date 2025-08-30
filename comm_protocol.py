"""
ASDM - Collaboration Protocol for ACD
-------------------------------------
Handles secure communication between controllers.
Supports state synchronization and threat intelligence sharing.
"""

import logging


class CollaborationProtocol:
    def __init__(self, controller_id: str):
        self.controller_id = controller_id
        self.peers = []  # List of peer controllers

    def add_peer(self, peer_id: str):
        """Register a peer controller for collaboration."""
        self.peers.append(peer_id)
        logging.info(f"[{self.controller_id}] Added peer: {peer_id}")

    def broadcast(self, message: dict):
        """
        Broadcast a message to all peers.
        In real system: use TLS-secured channels.
        """
        for peer in self.peers:
            logging.info(f"[{self.controller_id}] → {peer}: {message}")

    def share_state(self, state: str):
        """
        Share current defense state with peers.
        """
        message = {"controller": self.controller_id, "state": state}
        self.broadcast(message)
