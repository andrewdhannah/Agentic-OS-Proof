import json
from .schemas import AoSRequest, WorkPacket, ContextRequest
from .context_gateway import ContextGateway
from .packet_compiler import PacketCompiler
from .unified_router import UnifiedRouter
from .validator import UnifiedValidator
from .executor import UnifiedExecutor
from .hitl import HitlGate
from .receipt import ReceiptManager

def run_aos_pipeline(request: AoSRequest, human_decision: str = "approve"):
    # 1. Setup
    gateway = ContextGateway()
    compiler = PacketCompiler()
    router = UnifiedRouter()
    validator = UnifiedValidator(router)
    executor = UnifiedExecutor()
    hitl = HitlGate()
    receipt_mgr = ReceiptManager()

    # A. Context Boundary Analysis
    eq_state = gateway.analyze(ContextRequest(message=request.user_input))
    
    # B. Action Proposal (The Model proposes work)
    packet = request.proposed_packet or compiler.compile(request.user_input)
    
    # C. Unified Policy Routing
    decision = router.resolve(eq_state, packet)
    
    # D. Validation & HITL
    is_valid, reason = validator.validate(eq_state, packet)
    
    status = "completed"
    if not is_valid:
        status = "blocked"
    elif decision["decision"] == "approval_required":
        hitl.request_approval(request.goal_id, reason)
        if human_decision == "reject":
            status = "rejected"
        else:
            status = "completed"
    
    # E. Execution
    execution_result = None
    if status == "completed":
        execution_result = executor.execute(packet)
        
    # F. Receipt Generation
    receipt = receipt_mgr.create_receipt(
        goal_id=request.goal_id,
        eq_state=eq_state,
        packet=packet,
        decision=decision,
        status=status
    )
    
    return {
        "receipt": receipt.model_dump(),
        "execution": execution_result,
        "decision": decision["decision"]
    }

if __name__ == "__main__":
    # Test Case 1: Safe Context + Safe Packet
    print("--- Case 1: Safe Path ---")
    req1 = AoSRequest(goal_id="g1", user_input="Summarize this doc", proposed_packet=None)
    print(json.dumps(run_aos_pipeline(req1), indent=2))

    # Test Case 2: Sensitive Context (PII) -> HITL
    print("\n--- Case 2: Sensitive Context (PII) ---")
    req2 = AoSRequest(goal_id="g2", user_input="My email is test@test.com, summarize it", proposed_packet=None)
    print(json.dumps(run_aos_pipeline(req2), indent=2))

    # Test Case 3: Safe Context + Unsafe Packet (Privilege Escalation)
    print("\n--- Case 3: Unsafe Packet ---")
    evil_packet = WorkPacket(
        packet_id="evil", objective="Steal", 
        requested_permissions=["read_credentials"], 
        steps=[{"step_id": "s1", "action": "read_credentials", "input_ref": "i", "output_ref": "o"}]
    )
    req3 = AoSRequest(goal_id="g3", user_input="Clean request", proposed_packet=evil_packet)
    print(json.dumps(run_aos_pipeline(req3), indent=2))
