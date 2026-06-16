from .schemas import WorkPacket

class PacketCompiler:
    """
    Simplified Work Packet Compiler for the AOS Proof.
    In a real system, this would be the Large Model proposing work.
    """
    def compile(self, goal: str) -> WorkPacket:
        # In the real system, the LLM generates this.
        # For the POC, we simulate a "reasonable" proposal.
        return WorkPacket(
            packet_id=f"wp_{hash(goal)%1000}",
            objective=goal,
            requested_permissions=["read_fixture", "summarize_text_stub"],
            steps=[
                {"step_id": "s1", "action": "read_fixture", "input_ref": "input", "output_ref": "txt"},
                {"step_id": "s2", "action": "summarize_text_stub", "input_ref": "txt", "output_ref": "res"}
            ]
        )
