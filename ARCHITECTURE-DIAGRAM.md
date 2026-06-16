# Architecture Diagram: Agentic OS Unified Governance

## Mermaid.js Flow

```mermaid
graph TD
    User[User Goal] --> CG[Context Gateway]
    
    subgraph "Boundary 1: Context (Privacy)"
        CG -->|Senses PII/Risk| EQ[EQ State]
    end

    EQ --> UR[Unified Router]
    
    subgraph "Boundary 2: Action (Authority)"
        PC[Packet Compiler] -->|Proposes Steps| WP[Work Packet]
        WP --> UR
        Router[Permission Policy] -->|Grants| UR
    end

    UR --> Decision{Decision}
    
    Decision -->|Allowed| Exec[Constrained Executor]
    Decision -->|Approval Required| HITL[Human-in-the-Loop]
    Decision -->|Blocked| Abort[Abort & Log]
    
    HITL -->|Approved| Exec
    HITL -->|Rejected| Abort
    
    Exec --> Receipt[Unified Receipt]
    Abort --> Receipt
    
    style CG fill:#dfd,stroke:#333
    style PC fill:#ddf,stroke:#333
    style UR fill:#f9f,stroke:#333,stroke-width:4px
    style HITL fill:#fdd,stroke:#333
    style Receipt fill:#eee,stroke:#333
```

## Governance Logic

1. **Context Filter**: Before any work is proposed, the system determines the "State of the User" (Risk/PII).
2. **Delegation Proposal**: A "compiler" generates a structured request for work.
3. **Unified Check**: The Router asks: *"Given this specific user context, is this specific work packet authorized?"*
4. **Execution**: Work is performed only by a constrained executor that cannot deviate from the validated packet.
5. **Audit**: A single receipt proves the decision chain for both the information that crossed the boundary and the actions that were performed.
