# Test Matrix: Agentic OS Boundary Behavior

This matrix defines the expected behavior of the unified governance runtime.

| Context State | Proposed Packet | Decision | Expected Result | Proof Point |
|:---|:---|:---:|:---|:---|
| **Safe** (Low Risk, No PII) | **Safe** (Granted Perms) | `allowed` | ✅ Execute | Receipt: `context_validated=true`, `action_validated=true` |
| **Sensitive** (PII/Med Risk) | **Safe** (Granted Perms) | `approval_required` | ⏸️ HITL | Receipt: `approval_required=true`, `status=pending` |
| **Safe** (Low Risk, No PII) | **Unsafe** (Forbidden/Escalation) | `blocked` | ❌ Abort | Receipt: `action_boundary.packet_validated=false` |
| **Sensitive** (PII/Med Risk) | **Unsafe** (Forbidden/Escalation) | `blocked` | ❌ Abort | Receipt: `blocked_actions` listed |
| **Crisis** (High Risk) | **Any Packet** | `blocked` | ❌ Abort | Receipt: `route=blocked`, `reason=High risk context` |
| **Safe** (Low Risk) | **Dishonest** (Undeclared Action) | `blocked` | ❌ Abort | Receipt: `reason=dishonest_step` |
| **Any** | **Malformed** (Schema Fail) | `blocked` | ❌ Abort | Pydantic `ValidationError` |

**The Golden Rule:**
A model-proposed packet cannot override the context boundary, and a safe context cannot authorize an unsafe packet.
