from .schemas import WorkPacket, EqState
from .unified_router import UnifiedRouter

class UnifiedValidator:
    """
    Validates a proposal against the Unified Router.
    """
    def __init__(self, router: UnifiedRouter):
        self.router = router

    def validate(self, eq_state: EqState, packet: WorkPacket) -> tuple[bool, str]:
        decision = self.router.resolve(eq_state, packet)
        if decision["decision"] in ("allowed", "approval_required"):
            return True, "Validated"
        return False, decision["reason"]
