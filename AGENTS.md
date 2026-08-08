# Agent Development Contract

Every agent in EnterpriseOS follows a strict typed contract. Agents **recommend only** — they do not execute, approve, or modify business state.

## Agent Interface

```python
class Agent(ABC, Generic[InputT, OutputT]):
    name: str                          # Unique identifier
    description: str                   # Purpose & scope
    input_schema: type[InputT]         # Pydantic model
    output_schema: type[OutputT]       # Pydantic model
    instructions: str                  # Reasoning prompt
    confidence_threshold: float = 0.7  # Reject if below
    timeout_seconds: int = 30          # Hard 30s limit
    max_retries: int = 2               # Retry on transient errors
    dependencies: list["Agent"] = []   # Explicit dependency graph
    tools: list[object] = []           # Injected tools (repos, services)
    
    async def execute(self, raw_input: InputT | dict) -> OutputT:
        """Execute with validation, retry, timeout, confidence checks."""
        # 1. Validate input against input_schema
        # 2. Retry loop (max 3 attempts)
        # 3. Timeout (30s hard limit)
        # 4. Confidence threshold check (reject if below 0.7)
        # 5. Return OutputT or raise
```

## Agent Catalog

### 1. Planner Agent
| Property | Value |
|----------|-------|
| **Name** | `planner` |
| **Role** | Decomposes events into executable steps |
| **Input** | `BusinessEventInput` + `policy: PolicyDecision` |
| **Output** | `ExecutionPlan` (6 steps: classify→analyze→policy→approve→execute→audit) |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | All events; outputs gates, dependencies, parallel groups |
| **Reasoning** | "Create a timeline of work with resource owners, dependencies, and approval gates. Do not execute." |
| **Dependencies** | None |

**ExecutionPlan Output**:
```python
@dataclass
class PlanStep:
    order: int
    name: str
    owner: str  # "coo", "crisis", "approval_queue", etc.
    duration_minutes: int
    requires_approval: bool = False
    dependencies: list[int] = []

@dataclass
class ExecutionPlan:
    steps: list[PlanStep]
    estimated_duration_minutes: int
    approval_gates: list[str]  # ["human_approval"]
    parallel_groups: list[list[int]]  # [[2, 3]] if can run in parallel
```

---

### 2. COO Agent
| Property | Value |
|----------|-------|
| **Name** | `coo` |
| **Role** | Routes event to specialist agents; coordinates without executing |
| **Input** | `COOInput` (event + plan + policy) |
| **Output** | Routing dict: `{specialist_agents: [list], approval_required: bool}` |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | Crisis events → [crisis, finance, compliance]; Procurement → [procurement, finance, compliance] |
| **Reasoning** | "Select specialist agents, honor dependencies, aggregate recommendations. Do not execute side effects." |
| **Dependencies** | None (routes to others) |

**Routing Logic**:
- Event type `factoryfire`, `cyberattack`, `supplierbankruptcy`, `poweroutage`, `machinefailure`, `vendorbankruptcy` → `["crisis", "finance", "compliance"]`
- Event type `purchaserequest`, `vendordelay` → `["procurement", "finance", "compliance"]`
- Event type `equipmentfailure`, `employeeinjury`, `customerescalation` → `["operations", "finance", "compliance"]`

---

### 3. Procurement Agent
| Property | Value |
|----------|-------|
| **Name** | `procurement` |
| **Role** | Build procurement recommendation with vendor alternatives |
| **Input** | `BusinessEventInput` |
| **Output** | `Recommendation` (action, cost, alternatives, risk flags) |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | PurchaseRequest: analyze budget, urgency, quantity; recommend top vendor + alternatives |
| **Reasoning** | "Analyze quantity, urgency, budget, vendor alternatives, delivery risk. Recommend only." |
| **Dependencies** | `VendorIntelligence` (calls to rank vendors) |

**Output**:
```python
@dataclass
class Recommendation:
    action: str  # "Request quote from Vendor A"
    rationale: str
    confidence: float  # 0.0-1.0
    estimated_cost: float
    alternatives: list[VendorRecommendation]  # Top 3 ranked
    risk_flags: list[str]  # ["budget-missing", "supplier-continuity"]
    metadata: dict
```

---

### 4. Vendor Intelligence Agent
| Property | Value |
|----------|-------|
| **Name** | `vendor_intelligence` |
| **Role** | Rank vendors by delivery, cost, risk signals |
| **Input** | `VendorQuery` (category, quantity, urgency, budget, optional candidates) |
| **Output** | `list[VendorRecommendation]` (top 3 ranked) |
| **Confidence Threshold** | 0.50 (lower: best-effort ranking) |
| **Timeout** | 30s |
| **Key Scenarios** | Procurement, Crisis recovery; score on: 80% delivery, 10% cost, 10% risk |
| **Reasoning** | "Score delivery performance at 80%, cost competitiveness at 10%, and risk at 10%. Expose delay risk and alternatives." |
| **Dependencies** | None (self-contained ranking) |

**Scoring Formula**:
```
score = 0.8 * (on_time_rate) + 0.1 * (cost_competitiveness) + 0.1 * (1 - risk_rate)
```

**Output**:
```python
@dataclass
class VendorRecommendation:
    vendor_id: str
    vendor_name: str
    score: float  # 0.0-1.0
    estimated_cost: float
    delivery_days: int
    confidence: float
    risk_flags: list[str]  # ["delay-risk", "quality-issue"]
    reasoning: str = ""
```

---

### 5. Crisis Agent
| Property | Value |
|----------|-------|
| **Name** | `crisis` |
| **Role** | Analyze disruption impact, continuity, recovery |
| **Input** | `BusinessEventInput` (severity, payload) |
| **Output** | `CrisisRecommendation` (severity level 1-5, impact analysis, teams to activate, timeline) |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | FactoryFire, CyberAttack, SupplierBankruptcy: quantify exposure, identify recovery options, activate right teams |
| **Reasoning** | "Classify severity 1-5, quantify impact, identify recovery options, activate the right teams. Never execute." |
| **Dependencies** | `VendorIntelligence` (for supplier alternatives) |

**Output**:
```python
@dataclass
class CrisisRecommendation(Recommendation):
    severity_level: int  # 1-5
    impact_analysis: dict  # {daily_loss, employees_affected, products_affected}
    recovery_timeline_days: int
    teams_to_activate: list[str]  # ["operations", "compliance", "finance", "executive"]
```

---

### 6. Finance Agent
| Property | Value |
|----------|-------|
| **Name** | `finance` |
| **Role** | Validate funding, calculate annualized cost, escalate material spend |
| **Input** | `RecommendationInput` (event + recommendation + available_budget) |
| **Output** | `FinanceDecision` (approved/rejected/escalated, available budget, cost) |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | Any spend >$50K requires CFO escalation; available budget check; currency normalization |
| **Reasoning** | "Check available funds, normalize currency, calculate recurring 12-month impact, escalate material spend. Never release funds." |
| **Dependencies** | `BudgetRepository` (injected) |

**Output**:
```python
@dataclass
class FinanceDecision:
    status: str  # "approved", "rejected", "escalated"
    reasoning: str
    available_budget: float
    estimated_cost: float
    annualized_cost: float  # cost * 12 if recurring
    currency: str
    approval_role: str | None  # "CFO" if escalated
```

---

### 7. Compliance Agent
| Property | Value |
|----------|-------|
| **Name** | `compliance` |
| **Role** | Deterministic policy enforcement; check vendor/spending/safety controls |
| **Input** | `RecommendationInput` |
| **Output** | `ComplianceDecision` (compliant/non_compliant/escalated, violated rules, checked rules) |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | Vendor blacklist, audit holds, export restrictions, safety reviews, segregation of duties |
| **Reasoning** | "Check blacklists, audits, spending caps, safety controls, data handling, export restrictions. Return rule IDs." |
| **Dependencies** | `PolicyRepository` (injected) |

**Output**:
```python
@dataclass
class ComplianceDecision:
    status: str  # "compliant", "non_compliant", "escalated"
    reasoning: str
    violated_rules: list[str]  # ["POL-02", "POL-06"]
    controls_checked: list[str]  # All 10 controls evaluated
```

---

### 8. Operations Agent
| Property | Value |
|----------|-------|
| **Name** | `operations` |
| **Role** | Recommend operational remediation |
| **Input** | `BusinessEventInput` |
| **Output** | `Recommendation` (action, rationale, confidence) |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | Equipment failure, employee injury, customer escalation; assign owner, estimate resolution time |
| **Reasoning** | "Assess operational constraints, dependencies, owners, and recovery actions. Recommend only." |
| **Dependencies** | None |

---

### 9. Audit Agent
| Property | Value |
|----------|-------|
| **Name** | `audit` |
| **Role** | Capture immutable workflow transition evidence |
| **Input** | `BusinessEventInput` |
| **Output** | Audit dict: `{audited: bool, event_type: str, snapshots: [...]}`  |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | All events; records actor, transition, inputs, outputs, confidence, latency, tokens, approval state, state snapshot |
| **Reasoning** | "Record actor, transition, inputs, outputs, confidence, latency, tokens, approval state, and state snapshot. Never mutate business state." |
| **Dependencies** | None |

---

### 10. Notification Agent
| Property | Value |
|----------|-------|
| **Name** | `notification` |
| **Role** | Route role-aware notifications through channel adapters |
| **Input** | `BusinessEventInput` |
| **Output** | Delivery dict: `{queued: bool, channels: [...], audience_roles: [...]}`  |
| **Confidence Threshold** | 0.70 |
| **Timeout** | 30s |
| **Key Scenarios** | Email, Slack, SMS, Push based on urgency and role; retry transient failures |
| **Reasoning** | "Select email, Slack, SMS, or push based on urgency and recipient role. Retry transient failures. Never approve or execute." |
| **Dependencies** | `NotificationService` (injected) |

---

## Dependency Graph

```
BusinessEvent
  ↓
PlannerAgent → ExecutionPlan
  ↓
COOAgent (consumes plan) → specialist routing
  ↓
┌─────────────────────────────────────────────┐
│ Specialist Agents (selected by COO)         │
│                                             │
│ CrisisAgent ──┐                             │
│    ↓          │                             │
│ VendorIntel   └─ Finance ┐                  │
│                           │                 │
│ ProcurementAgent ────────→├─ Compliance   │
│                    ↓       │                 │
│                VendorIntel │                 │
│                           └─ Operations    │
└─────────────────────────────────────────────┘
     ↓ (all agents finish)
PolicyEngine (deterministic rules)
     ↓
ApprovalQueue (human interrupt)
     ↓
ExecutionCommands (external only)
     ↓
AuditAgent → AuditLog (immutable record)
     ↓
NotificationAgent → Email/Slack
```

**Ordering Rules**:
1. No agent has circular dependencies
2. VendorIntelligence is idempotent (can be called multiple times)
3. Finance and Compliance can run in parallel (no shared state)
4. Policy checks happen BEFORE any approval (non-bypassable)
5. Audit and Notification happen AFTER approval decision

---

## Typing Rules

### Pydantic Models (in `app/schemas/agents.py`)

All inputs/outputs must be Pydantic `BaseModel`:
- **Field validation**: min/max length, ge/le ranges
- **Defaults**: Optional fields have `None` or sensible defaults
- **Serialization**: All models support `.model_dump()` and `.model_validate()`
- **No raw dicts**: Always use typed models

### Confidence Scoring

Every agent that returns a `Recommendation` includes confidence: `0.0` (no confidence) to `1.0` (certain).

**Interpretation**:
- `confidence >= threshold` → accept recommendation
- `confidence < threshold` → reject with `ValueError(f"{agent_name} confidence below threshold")`
- `confidence == 1.0` → human approval may be waived (but policy still blocks if needed)

### Timeouts

**Hard 30s limit** enforced via `asyncio.wait_for()`:
- If agent task exceeds 30s, `TimeoutError` is raised
- Agent retries up to 2 times on timeout
- After max retries, recommendation is rejected

### Retry Policy

```python
AsyncRetrying(
    stop=stop_after_attempt(3),  # 1 initial + 2 retries
    wait=wait_exponential(multiplier=0.2, min=0.2, max=2),  # 0.2s, 0.4s, 0.8s, 1.2s, 1.6s, 2s
    retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    reraise=True
)
```

**Retryable exceptions**: `TimeoutError`, `ConnectionError`
**Non-retryable**: Validation errors, confidence checks, policy violations

---

## Execution Semantics

### Agent No-Ops
Agents **must not**:
- ❌ Modify database directly
- ❌ Send emails/Slack messages
- ❌ Execute orders or payments
- ❌ Bypass policy gates
- ❌ Hold state across invocations
- ❌ Access real LLM if API keys missing (use in-memory defaults)

### Allowed Operations
Agents **can**:
- ✅ Read from injected repositories (VendorRepository, BudgetRepository, etc.)
- ✅ Call other agents (dependency resolution)
- ✅ Call LLM service for structured reasoning
- ✅ Return recommendations with confidence & rationale
- ✅ Emit side-effect-free observability (metrics, logs)

### Output Guarantees
All agent outputs must:
1. Be serializable to JSON (Pydantic `.model_dump()`)
2. Fit within audit log (max ~10KB per agent output)
3. Contain rationale human-readable and testable
4. Include confidence score where applicable

---

## Testing Contract

### Unit Tests
Each agent has a corresponding test in `tests/agents/test_*.py`:
```python
@pytest.mark.asyncio
async def test_procurement_agent_execution():
    agent = ProcurementAgent()
    input_data = BusinessEventInput(
        event_type="PurchaseRequest",
        title="Emergency compressor",
        description="...",
        payload={"quantity": 1, "urgency": "high", "budget": 20000}
    )
    result = await agent.execute(input_data)
    
    assert isinstance(result, Recommendation)
    assert result.confidence >= 0.3  # Allow low confidence in tests
    assert len(result.alternatives) > 0
    assert result.estimated_cost <= 20000
```

### Integration Tests
End-to-end workflow in `tests/integration/test_workflow_paths.py`:
- Event ingestion → classification → planning → specialist execution → audit logging
- Verify output of each agent fed correctly to next stage
- Verify policy blocks non-compliant recommendations

### Load Tests
Concurrent workflow execution in `tests/load/test_concurrent_workflows.py`:
- 10+ concurrent events in flight
- Verify connection pooling, queue handling, retry logic under load

---

## Configuration & Defaults

Each agent loads configuration from environment (optional):
```python
AGENT_TIMEOUT_SECONDS=30  # Default
AGENT_CONFIDENCE_THRESHOLD=0.7  # Default
LLM_FALLBACK_TO_DEFAULTS=true  # If true, use in-memory repos when LLM keys missing
```

No agent should require secrets beyond what is set in `.env`.

---

## Documentation Requirements

Each agent must document:
1. **Name & Description**: 1-2 sentence purpose
2. **Input & Output**: Pydantic model names + key fields
3. **Confidence Threshold**: When to reject
4. **Timeout & Retries**: 30s hard limit, 2 retries
5. **Key Scenarios**: 3-4 examples of when this agent activates
6. **Dependencies**: Explicit list of other agents or repositories it depends on
7. **Determinism**: Whether output is deterministic (no randomness)
8. **LLM Usage**: If agent calls LLM, note fallback behavior

---

## Compliance Checklist

- ✅ All agents inherit from `Agent[InputT, OutputT]`
- ✅ All inputs/outputs are Pydantic models
- ✅ `name`, `description`, `input_schema`, `output_schema` are defined
- ✅ `instructions` prompt provided (what agent should do)
- ✅ `confidence_threshold` set (default 0.70)
- ✅ `timeout_seconds` = 30 (hard limit)
- ✅ `max_retries` = 2 (3 attempts total)
- ✅ `dependencies` list explicit (even if empty)
- ✅ No database mutations in `run()` method
- ✅ All side effects (email, Slack) delegated to NotificationAgent
- ✅ All execution deferred to external executor, never in agent
- ✅ Output includes rationale + confidence (where applicable)
- ✅ Tests exist in `tests/agents/test_*.py`