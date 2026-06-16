from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# --- Context Boundary (EQ Gateway) ---

class EqState(BaseModel):
    """Structured metadata about the user's emotional and privacy state."""
    affect: str = "neutral"
    intent: str = "unknown"
    risk_level: str = "low" # low, medium, high
    pii_detected: bool = False
    raw_text_allowed: bool = False

class ContextRequest(BaseModel):
    message: str
    session_id: str = "default"

# --- Action Boundary (Work Packet Compiler) ---

class WorkStep(BaseModel):
    step_id: str
    action: str
    input_ref: str
    output_ref: str

class WorkPacket(BaseModel):
    model_config = ConfigDict(frozen=True)
    packet_id: str
    objective: str
    requested_permissions: List[str] = []
    steps: List[WorkStep]

# --- Unified Governance ---

class UnifiedReceipt(BaseModel):
    """The definitive proof of the governed runtime."""
    receipt_id: str
    goal_id: str
    context_boundary: Dict[str, Any]
    action_boundary: Dict[str, Any]
    human_authority: Dict[str, Any]
    final_status: str # completed, blocked, rejected, pending
    timestamp: str

class AoSRequest(BaseModel):
    """The entry point to the Agentic OS."""
    goal_id: str
    user_input: str
    proposed_packet: Optional[WorkPacket] = None
