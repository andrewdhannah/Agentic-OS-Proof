from typing import Dict, Any
from .schemas import WorkPacket

class UnifiedExecutor:
    """
    Constrained Executor that only runs if the combined boundaries are cleared.
    """
    def __init__(self):
        self.state: Dict[str, Any] = {}

    def execute(self, packet: WorkPacket) -> str:
        # Boring implementation of a few actions
        results = []
        for step in packet.steps:
            if step.action == "read_fixture":
                res = f"Reading {step.input_ref}..."
            elif step.action == "summarize_text_stub":
                res = f"Summarizing {step.input_ref}..."
            else:
                res = f"Executing {step.action}..."
            
            self.state[step.output_ref] = res
            results.append(res)
        
        return " | ".join(results)
