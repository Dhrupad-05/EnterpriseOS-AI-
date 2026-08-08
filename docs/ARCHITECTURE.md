# EnterpriseOS AI - Architecture

## System Overview

EnterpriseOS AI is an event-driven enterprise operations platform implementing the separation: **AI recommends → Policy governs → Humans approve → Executors perform**.

```
┌─────────────────────────────────────────────────────────────┐
│                    Business Event Intake                    │
│  (Procurement, Vendor, Incident, Finance, Compliance)       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              Event Classification Service                   │
│    (Normalizes input, extracts event type & severity)       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│         LangGraph Workflow Orchestrator                     │
│  ┌──────────┐  ┌─────────┐  ┌────────────┐  ┌──────────┐    │
│  │ Planner  │→ │ Policy  │→ │ Specialist │→ │Approval  │    │
│  │ Agent    │  │ Engine  │  │ Agents     │  │ Interrupt│    │
│  └──────────┘  └─────────┘  └────────────┘  └──────────┘    │
│         ↓ (policy reject)                         ↓         │
│         └──────────────→ Audit & Archive ←───────┘          │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼───────┐         ┌──────────▼────────┐
│ PostgreSQL    │         │ Redis Cache       │
│ (Persistence) │         │ (Checkpoints)     │
└───────────────┘         └───────────────────┘
        │
┌───────▼──────────────────────────────────────┐
│ Audit Log (immutable timeline)               │
│ - State snapshots at each step               │
│ - Decision records with confidence           │
│ - Replay capability without re-execution     │
└──────────────────────────────────────────────┘
```

## Core Components

### 1. FastAPI Backend (`app/main.py`)
- **Role**: HTTP entry point for events, approvals, workflows
- **Routes**:
  - `POST /api/v1/events` → Ingest business event
  - `POST /api/v1/events/{id}/orchestrate` → Run workflow
  - `GET /api/v1/approvals` → List pending decisions
  - `POST /api/v1/approvals/{id}/decision` → Record approval
  - `GET /api/v1/workflows/{id}/replay` → Audit timeline
  - `GET /api/v1/system/metrics/prometheus` → Observability

### 2. Event Service (`app/services/events.py`)
**Responsibilities**:
- Parse incoming business events
- Classify event type (Purchase, Vendor, Incident, Compliance, Finance)
- Create `BusinessEvent` entity
- Initialize `WorkflowInstance`
- Publish domain events

**Event Classification Mapping**:
```python
{
  "PURCHASEREQUEST": "PROCUREMENT",
  "VENDORDELAY": "PROCUREMENT",
  "VENDORBANKRUPTCY": "CRISIS",
  "FACTORYFIRE": "CRISIS",
  "CYBERATTACK": "CRISIS",
  "EQUIPMENTFAILURE": "OPERATIONS",
  "COMPLIANCEISSUE": "COMPLIANCE",
  "BUDGETOVERAGE": "FINANCE"
}
```

### 3. LangGraph Orchestrator (`app/workflows/graph.py`)
**Master State Machine**:

```
CREATED
  ↓
CLASSIFIED (EventService)
  ↓
PLANNING (PlannerAgent decomposes into steps)
  ↓
POLICY_CHECK (PolicyEngine evaluates rules)
  ├→ REJECTED (policy blocks) → AUDIT
  │
  ├→ SPECIALISTS (Crisis, Procurement, Finance, Compliance agents)
  │   ├→ Finance rejects budget → AUDIT
  │   ├→ Compliance rejects policy → AUDIT
  │
  ├→ AWAITING_APPROVAL (interrupt with context)
  │   ├→ APPROVED (human decision) → EXECUTING
  │   ├→ REJECTED → AUDIT
  │   ├→ EXPIRED → AUDIT
  │
  ├→ EXECUTING (external executor only)
  │
  ├→ MONITORING (optional health checks)
  │
  └→ COMPLETED
       ↓
    ARCHIVED
```

**Graph Nodes**:
1. `classify` - Mark as classified, log audit entry
2. `plan` - Execute PlannerAgent, emit execution steps
3. `policy` - Run PolicyEngine, evaluate against rules
4. `specialists` - Parallel agents (Crisis, Procurement, Finance, Compliance, Operations, COO)
5. `approval` - Call `interrupt()` to pause workflow
6. `execute` - Emit commands (never execute directly)
7. `audit` - Record final state, increment metrics

### 4. Policy Engine (`app/services/policy.py`)
**Deterministic Governance**:
- 5 built-in rules: Budget threshold, Vendor blacklist, Crisis escalation, Refund approval, Inventory reorder
- Rules are data-backed (not hardcoded in agents)
- Each rule has: ID, priority, matcher, evaluator
- Returns: `PolicyDecision(status, reason, matched_rules, required_approval_role)`

**Rule Priority**:
1. Vendor blacklist (reject immediately)
2. Crisis severity >3 (escalate to CEO)
3. Budget >$50K (escalate to Finance)
4. Refund >$1K (escalate to Manager)
5. Inventory <10% (escalate to Operations)

### 5. Specialist Agents
Each agent is a typed `Agent[InputModel, OutputModel]`:

| Agent | Input | Output | Timeout | Confidence |
|-------|-------|--------|---------|------------|
| Planner | BusinessEventInput | ExecutionPlan | 30s | 0.70 |
| COO | COOInput (event+plan+policy) | routing dict | 30s | 0.70 |
| Procurement | BusinessEventInput | Recommendation | 30s | 0.70 |
| VendorIntelligence | VendorQuery | list[VendorRecommendation] | 30s | 0.50 |
| Crisis | BusinessEventInput | CrisisRecommendation | 30s | 0.70 |
| Finance | RecommendationInput | FinanceDecision | 30s | 0.70 |
| Compliance | RecommendationInput | ComplianceDecision | 30s | 0.70 |
| Operations | BusinessEventInput | Recommendation | 30s | 0.70 |
| Audit | BusinessEventInput | audit dict | 30s | 0.70 |
| Notification | BusinessEventInput | delivery plan | 30s | 0.70 |

**Agent Contract** (`app/agents/contract.py`):
```python
class Agent(ABC, Generic[InputT, OutputT]):
    name: str
    description: str
    input_schema: type[InputT]
    output_schema: type[OutputT]
    instructions: str
    confidence_threshold: float = 0.7
    timeout_seconds: int = 30
    max_retries: int = 2
    dependencies: list["Agent"] = []
    
    async def execute(self, raw_input) -> OutputT:
        # Validation → Retry loop → Confidence check → Timeout enforcement
```

**Retry Strategy**: Exponential backoff (0.2s→2s), retry on TimeoutError/ConnectionError only.

### 6. Approval Queue (`app/approvals/queue.py` + `service.py`)
**Human-in-the-Loop**:
- Workflow pauses at `approval` node via `interrupt()`
- Approval request stored in PostgreSQL with 30min expiry
- Resume via `POST /api/v1/approvals/{id}/decision`
- Decision (approved/rejected/modified) + comment logged
- Workflow resumes with Command(resume={decision, comment})

**Cannot skip policy or approval**: Approval node checks status after human decision.

### 7. Workflow Persistence (`app/workflows/persistence.py`)
**Durable State**:
- `WorkflowInstance` stores current step, state snapshot, timestamps
- `AuditLog` records every transition with decision, confidence, latency, tokens
- Redis caches snapshots for fast load (optional)
- PostgreSQL is authoritative

**Replay**: Load audit timeline, show all decisions + snapshots without re-executing.

### 8. LLM Service (`app/services/llm.py`)
**Provider Fallback Chain**:
```
Gemini (primary, $0 cost in demo)
  ↓ (timeout/failure)
Groq (fast, $0.24/$0.24 per 1M tokens)
  ↓ (timeout/failure)
OpenRouter (fallback, $0.08/$0.08 per 1M tokens)
```

**Structured Output**: All agents call `llm_service.call_structured(prompt, schema)` → Returns typed Pydantic model.

**Determinism**: If all LLM keys are missing, agents use repository-backed defaults (in-memory mock data).

### 9. Notification Service (`app/notifications/service.py`)
**Role-Aware Delivery**:
- Email (Resend API)
- Slack (Bot API)
- SMS/Push (pluggable)
- Retry policy: 3 attempts, exponential backoff
- Channels are injected at init (not hardcoded)

### 10. Repository Pattern (`app/repositories/`)
**Data Access Contracts**:
- `BudgetRepository`: `department_budget()`, `spending_to_date()`
- `VendorRepository`: `get_vendor_metrics()`, `list_by_category()`
- `PolicyRepository`: `active()` policies
- `IncidentRepository`: `employees_affected()`, `alternatives()`
- `ProductRepository`: `by_supplier()`, `by_factory()`

**In-Memory Defaults**: All repos have `InMemory*` implementations for local testing.

## Data Model

### Core Entities (`app/models/entities.py`)

```python
class BusinessEvent:
    id: UUID
    event_type: str  # "VendorBankruptcy", "PurchaseRequest", etc.
    classification: str  # "CRISIS", "PROCUREMENT", "OPERATIONS", etc.
    title: str
    description: str
    severity: str  # "low", "medium", "high", "critical"
    status: EventStatus  # CREATED → CLASSIFIED → ... → COMPLETED
    payload: dict  # Event-specific data
    workflow_id: UUID → Workflow
    created_by: UUID → User

class Approval:
    id: UUID
    event_id: UUID → BusinessEvent
    proposed_action: dict  # The recommendation being approved
    status: ApprovalStatus  # PENDING → APPROVED/REJECTED/MODIFIED
    requested_by: UUID → User
    decided_by: UUID → User (nullable)
    expires_at: datetime
    comment: str (nullable)
    urgency: str  # "normal", "critical"

class AuditLog:
    id: UUID
    event_id: UUID → BusinessEvent
    action: str  # "classified", "approved", "rejected", "executed"
    decision: dict  # The actual decision made
    confidence: float (nullable)
    latency_ms: int (nullable)
    tokens: int (nullable)
    correlation_id: str  # trace to workflow_id

class WorkflowInstance:
    id: UUID
    event_id: UUID → BusinessEvent
    status: str  # Current state (CLASSIFIED, PLANNING, etc.)
    current_step: str  # Node name in graph
    state_snapshot: dict  # Full workflow state
    started_at: datetime
    completed_at: datetime (nullable)
```

### Operations Entities (`app/models/operations.py`)

```python
class Vendor:
    name: str
    category: str  # "Raw materials", "Freight", etc.
    risk_score: float  # 0-100
    performance_score: float
    on_time_delivery_rate: float
    avg_unit_cost: float
    avg_delivery_days: int
    late_deliveries_90d: int
    metadata: dict

class PurchaseOrder:
    vendor_id: UUID → Vendor
    amount: float
    currency: str  # "USD", etc.
    status: str  # "draft", "approved", "shipped"
    line_items: list[dict]

class Incident:
    event_id: UUID → BusinessEvent
    category: str  # "Cyber Attack", "Factory Fire", etc.
    impact: str
    severity: str
    response_plan: dict

class Equipment:
    asset_id: UUID → Asset
    serial_number: str
    health_score: float  # 0-1
```

## API Flow Example: Vendor Bankruptcy Crisis

```
1. POST /api/v1/events
   {
     "event_type": "VendorBankruptcy",
     "severity": "critical",
     "payload": {
       "vendor_id": "v-001",
       "daily_loss": 2300000,
       "employees_affected": 500,
       "recovery_budget": 100000
     }
   }

2. EventService.ingest()
   - Create BusinessEvent(status=CREATED)
   - Classify → "CRISIS"
   - Create WorkflowInstance(status=CLASSIFIED)
   - Return event_id

3. POST /api/v1/events/{event_id}/orchestrate
   - Load BusinessEvent
   - Build WorkflowOrchestrator graph
   - Invoke graph.ainvoke({"event": {...}})
   
   Graph execution:
   a) classify() → audit log
   b) plan() → PlannerAgent emits 6-step recovery plan
   c) policy() → PolicyEngine matches CRISIS-CEO rule
   d) specialists() → Crisis, Finance, Compliance agents run in parallel
      - CrisisAgent: severity=5, daily_loss=$2.3M, alternatives=[vendors]
      - FinanceAgent: escalation required ($100K)
      - ComplianceAgent: no violations
   e) approval() → interrupt() pauses graph, returns approval context
   
4. Response:
   {
     "event_id": "uuid",
     "status": "awaiting_approval",
     "interrupt": true,
     "recommendations": {
       "crisis": {...},
       "finance": {...},
       "compliance": {...}
     }
   }

5. GET /api/v1/approvals
   → Returns pending approval with 30min countdown

6. POST /api/v1/approvals/{approval_id}/decision
   {
     "status": "approved",
     "comment": "Approved recovery plan. Activate team."
   }
   - Update Approval.status = APPROVED
   - Resume graph via Command(resume={decision: "approved"})
   
   Graph resumes:
   f) execute() → Emit execution commands (no side effects)
   g) audit() → Record final state, increment WORKFLOWS metric
   
7. GET /api/v1/workflows/{workflow_id}/replay
   → Timeline:
     [04:12:03] Incident detected (VendorBankruptcy)
     [04:12:11] Crisis Agent engaged
     [04:14:52] Approval requested
     [04:16:30] Approved by Manager
     [04:17:05] Executing recovery
```

## Security & Governance

1. **Authentication**: JWT tokens (access + refresh), OAuth2PasswordBearer
2. **Authorization**: Role-based access (CEO, Finance, Operations, etc.)
3. **Audit Trail**: Every action immutable in AuditLog
4. **Policy Isolation**: Rules checked before approval, cannot be bypassed
5. **No Side Effects in Agents**: LLM is read-only, returns recommendations only
6. **Secrets**: Environment-only configuration, never committed

## Observability

**Prometheus Metrics**:
- `enterpriseos_workflows_total{status, event_type}` → Workflow outcomes
- `enterpriseos_agent_executions_total{agent, status}` → Agent results
- `enterpriseos_agent_latency_ms{agent}` → Latency histogram
- `enterpriseos_approvals_total{decision}` → Approval decisions

**Structured Logging**: Correlation ID propagated through entire workflow for tracing.

**Health Checks**: `/health` endpoint validates database and Redis connectivity.

## Deployment

**Docker Compose** (`docker-compose.yml`):
- `backend`: FastAPI app on :8000
- `postgres`: PostgreSQL 16 (async SQLAlchemy)
- `redis`: Redis 7 (checkpoint storage)

**Environment Config** (`.env`):
- Database: `postgresql+asyncpg://...`
- Redis: `redis://...`
- LLM Keys: `GEMINI_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY`
- Notifications: `RESEND_API_KEY`, `SLACK_BOT_TOKEN`

**Database Migrations** (`alembic/`):
- Async SQLAlchemy with Alembic
- Single migration: `0001_initial_schema.py` creates all tables
- Run on startup: `alembic upgrade head`

## Design Decisions (ADRs)

1. **Event-Driven**: Single intake model, not department-specific workflows
2. **Policy Isolation**: Deterministic rules before LLM recommendations
3. **Approval Interrupts**: LangGraph `interrupt()` for human-in-the-loop
4. **LangGraph Subgraphs**: Each agent wrapped in isolated subgraph
5. **Audit Replay**: State snapshots enable investigation without re-execution

## Performance Targets

- **Classification**: <1s (event service)
- **Policy Check**: <1s (deterministic rules)
- **Agent Chain**: <30s total (3 agents × 10s typical)
- **Approval**: 30min default timeout
- **Replay**: <5s (load from audit log, no re-execution)
- **Concurrent Workflows**: 100+ (async FastAPI, connection pooling)