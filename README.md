# Agentic OS Proof

## Governed Runtime for AI Agents

The Agentic OS Proof is an integration harness that demonstrates the composition of two fundamental boundaries: the **Context Boundary** (EQ Gateway) and the **Action Boundary** (Work Packet Compiler).

### The Thesis: Unified Governance
A safe agentic system requires a dual-gate architecture. Intelligence is decoupled from Authority across two distinct planes:

1. **Context Boundary:** What information may cross the device boundary? (Analyzed via EQ State).
2. **Action Boundary:** What work is allowed to happen? (Analyzed via Work Packets).

A request is only executed if it passes **both** boundaries.

### AOS-1: Integration Harness
The goal of this phase is to prove that these two boundaries compose cleanly into a single governed runtime.

**Core Pipeline:**
`User Goal` $\rightarrow$ `Context Analysis (EQ)` $\rightarrow$ `Action Proposal (WPC)` $\rightarrow$ `Unified Policy Routing` $\rightarrow$ `HITL Approval` $\rightarrow$ `Constrained Execution` $\rightarrow$ `Unified Receipt`

### Key Proof Points
- **Dual-Gate Enforcement:** A valid work packet cannot bypass a privacy violation in the context boundary.
- **Unified Receipt:** A single audit trail proving both the context state and the action authorization.
- **Human Authority:** A single HITL gate that can block the entire pipeline based on the combined risk of context and action.

---

## Related Proofs
This project is part of a broader agentic AI safety architecture:
- [EQ Gateway](https://github.com/andrewdhannah/EQ-Gateway) — Context Boundary / Privacy Firewall
- [Work Packet Compiler](https://github.com/andrewdhannah/Work-Packet-Compiler) — Action Boundary / Governed Delegation
- [Agentic OS Proof](https://github.com/andrewdhannah/Agentic-OS-Proof) — Integrated Governance Runtime (This project)

