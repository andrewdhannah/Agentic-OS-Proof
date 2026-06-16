class HitlGate:
    """
    Simple Human-in-the-Loop gate.
    In a real system, this would be a persistent state waiting for a webhook.
    """
    def __init__(self):
        self.pending = {}

    def request_approval(self, request_id: str, reason: str):
        self.pending[request_id] = {"status": "pending", "reason": reason}
        return f"PENDING: {reason}"

    def resolve(self, request_id: str, decision: str):
        if request_id in self.pending:
            self.pending[request_id]["status"] = decision
            return decision
        return "error: request_id not found"
