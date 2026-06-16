from .schemas import ContextRequest, EqState

class ContextGateway:
    """
    Simplified EQ Gateway for the AOS Proof.
    Simulates the local privacy firewall.
    """
    def analyze(self, request: ContextRequest) -> EqState:
        # Simulation of local SLM analysis
        text = request.message.lower()
        
        # Basic PII simulation
        pii = "email" in text or "phone" in text or "address" in text
        
        # Risk simulation
        risk = "low"
        if "crisis" in text or "harm" in text:
            risk = "high"
        elif "angry" in text or "frustrated" in text:
            risk = "medium"
            
        # Permission based on risk
        raw_allowed = (risk == "low" and not pii)
        
        return EqState(
            affect="frustrated" if risk == "medium" else "neutral",
            intent="request" if "want" in text else "query",
            risk_level=risk,
            pii_detected=pii,
            raw_text_allowed=raw_allowed
        )
