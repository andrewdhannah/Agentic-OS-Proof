from typing import Set, Dict, Any
from .schemas import EqState, WorkPacket

class UnifiedRouter:
    """
    The Master Policy Engine.
    Combines Context Boundary and Action Boundary into a single decision.
    """
    def __init__(self):
        self.granted_permissions = {"read_fixture", "summarize_text_stub", "write_artifact_stub"}
        self.hard_forbidden = {"delete_file", "send_network_request", "modify_policy"}

    def resolve(self, eq_state: EqState, packet: WorkPacket) -> Dict[str, Any]:
        # 1. Context-Based Blocking
        if eq_state.risk_level == "high":
            return {"decision": "blocked", "reason": "High risk context detected"}

        # 2. Permission-Based Blocking
        requested = set(packet.requested_permissions)
        unauthorized = requested - self.granted_permissions
        if unauthorized:
            return {"decision": "blocked", "reason": f"Unauthorized permissions: {unauthorized}"}

        # 3. Action-Based Blocking (Hard Forbidden)
        step_actions = {s.action for s in packet.steps}
        forbidden = step_actions & self.hard_forbidden
        if forbidden:
            return {"decision": "blocked", "reason": f"Forbidden actions: {forbidden}"}

        # 4. HITL Decision
        # If context is medium risk OR pii is detected, we require human approval
        if eq_state.risk_level == "medium" or eq_state.pii_detected:
            return {"decision": "approval_required", "reason": "Sensitivity/Risk requires HITL"}

        return {"decision": "allowed", "reason": "All boundaries cleared"}
