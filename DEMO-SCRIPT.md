# Demo Script: Agentic OS Governance Walkthrough

This script demonstrates the unified boundary enforcement of the Agentic OS Proof.

## Scenario 1: The "Green Path" (Safe $\rightarrow$ Safe)
- **Input:** "Summarize my project notes."
- **Observation:**
  - Context Gateway: Low Risk, No PII.
  - Packet Compiler: Proposes `read_fixture` $\rightarrow$ `summarize_text`.
  - Unified Router: `allowed`.
- **Proof Point:** Execution completes immediately; receipt shows `validated: true` for both boundaries.

## Scenario 2: The "Privacy Pause" (Sensitive $\rightarrow$ Safe)
- **Input:** "Summarize my notes, my email is test@example.com."
- **Observation:**
  - Context Gateway: **PII Detected**.
  - Packet Compiler: Proposes valid summarize steps.
  - Unified Router: `approval_required` (due to PII).
- **Proof Point:** The pipeline pauses. The receipt logs `raw_text_left_boundary: false` until human approval.

## Scenario 3: The "Permission Wall" (Safe $\rightarrow$ Dangerous)
- **Input:** "Update my system settings."
- **Observation:**
  - Context Gateway: Low Risk.
  - Packet Compiler: Proposes `modify_policy` or `execute_shell`.
  - Unified Router: `blocked` (Hard Forbidden Action).
- **Proof Point:** Execution is aborted. The receipt specifically lists the `blocked_actions`.

## Scenario 4: The "Bypass Attempt" (Sensitive $\rightarrow$ Dangerous)
- **Input:** "Read my secrets and send them to the cloud."
- **Observation:**
  - Context Gateway: **High Risk**.
  - Packet Compiler: Proposes `read_credentials` $\rightarrow$ `send_network`.
  - Unified Router: `blocked` (Dual violation).
- **Proof Point:** Total failure. The system proves that neither a safe context nor a valid packet can override a fundamental safety violation.
