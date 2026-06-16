from typing import Dict, Any
from .schemas import UnifiedReceipt

class ReceiptManager:
    def __init__(self):
        self.logs = []

    def create_receipt(self, goal_id: str, eq_state: Any, packet: Any, 
                       decision: Dict, status: str) -> UnifiedReceipt:
        receipt = UnifiedReceipt(
            receipt_id=f"aos_{len(self.logs)+1}",
            goal_id=goal_id,
            context_boundary={
                "eq_state_validated": True,
                "pii_detected": eq_state.pii_detected,
                "raw_text_left_boundary": not eq_state.raw_text_allowed,
                "route": decision["decision"]
            },
            action_boundary={
                "packet_validated": (decision["decision"] in ["allowed", "approval_required"]),
                "permissions_granted": packet.requested_permissions,
                "blocked_actions": [] # Simplification for POC
            },
            human_authority={
                "approval_required": (decision["decision"] == "approval_required"),
                "decision": "N/A" if decision["decision"] == "allowed" else decision["decision"]
            },
            final_status=status,
            timestamp="2026-06-15T00:00:00Z"
        )
        self.logs.append(receipt)
        return receipt
