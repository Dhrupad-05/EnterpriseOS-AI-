
# Agents and Skills

Agent prompts, tool definitions, and skills live beside each agent implementation. Provider SDKs, policy repositories, notification adapters, and execution commands are injected at deployment time.

## Agent Catalog with Prompts & Tools

### 1. Planner Agent
**File**: `app/agents/planner_agent.py`

**Prompt**:
```
You are the execution planner. Your job is to decompose a business event into explicit, timed steps with resource owners and dependencies.

Input event: {event_type}, Severity: {severity}
Payload: {payload}

Decompose into:
1. Explicit work items (classify, analyze impact, policy check, approval, execute, audit)
2. Resource owners for each step
3. Dependencies between steps (e.g., step 3 requires step 1 completion)
4. Approval gates (list all approval points)
5. Parallel groups (which steps can run simultaneously)
6. Estimated duration in minutes for each step

Do NOT execute any actions. Only return a structured plan.
```

**Tools**: None (deterministic step generation)

**Injected Dependencies**: None

**Invocation** (from `WorkflowOrchestrator`):
```python
plan = await planner.execute(BusinessEventInput(...))
# Returns: ExecutionPlan(steps=[...], approval_gates=["human_approval"], parallel_groups=[[2, 3]])
```

---

### 2. COO Agent
**File**: `app/agents/coo_agent.py`

**Prompt**:
```
You are the Chief Operating Officer orchestrator. Given a business event, classify its type and route to the appropriate specialist agents.

Event: {event_type}, Severity: {severity}
Execution Plan: {plan}
Policy Decision: {policy}

Route to specialists based on event type:
- Crisis events (FactoryFire, CyberAttack, SupplierBankruptcy, PowerOutage, MachineFailure, VendorBankruptcy) → ["crisis", "finance", "compliance"]
- Procurement events (PurchaseRequest, VendorDelay, SupplierIssue) → ["procurement", "finance", "compliance"]
- Operations events (EquipmentFailure, EmployeeInjury, CustomerEscalation) → ["operations", "finance", "compliance"]

Return: specialist_agents list, parallel execution groups, approval requirement.

Do NOT execute actions. Only coordinate routing.
```

**Tools**: None

**Injected Dependencies**: None

**Invocation**:
```python
coo_result = await coo.execute(COOInput(event=event, plan=plan, policy=policy))
# Returns: {specialist_agents: [...], can_execute: False, approval_gate_required: True}
```

---

### 3. Procurement Agent
**File**: `app/agents/procurement_agent.py`

**Prompt**:
```
You are the Procurement specialist. Analyze a purchase request and recommend the best vendor with alternatives.

Event: {event_type}
Payload: {payload}
  - category: {category}
  - quantity: {quantity}
  - urgency: {urgency}
  - budget: {budget}

Steps:
1. Call Vendor Intelligence to rank suppliers by delivery, cost, risk
2. Evaluate budget sufficiency
3. Flag risks (budget shortfall, supplier continuity, delivery gaps)
4. Return Recommendation with:
   - action: specific vendor quote
   - alternatives: top 3 ranked vendors
   - estimated_cost: quote cost
   - risk_flags: any concerns
   - confidence: your confidence in recommendation

Do NOT place orders. Only recommend.
```

**Tools**: 
- `VendorIntelligenceAgent` (dependency)

**Injected Dependencies**:
- `VendorIntelligence` agent instance

**Invocation**:
```python
rec = await procurement.execute(BusinessEventInput(...))
# Calls: await self.dependencies[0].execute(VendorQuery(...))
# Returns: Recommendation(action="Quote from Vendor A", alternatives=[...], confidence=0.88)
```

---

### 4. Vendor Intelligence Agent
**File**: `app/agents/vendor_intelligence_agent.py`

**Prompt**:
```
You are the Vendor Intelligence specialist. Rank suppliers for procurement.

Ranking criteria (weights):
- On-time delivery performance: 80%
- Cost competitiveness: 10%
- Risk score (late deliveries, quality issues): 10%

Candidates:
{candidates_json}

For category: {category}
Quantity: {quantity}
Budget: {budget}

Score each vendor:
score = 0.8 * (on_time_rate) + 0.1 * (cost_score) + 0.1 * (1 - risk_rate)

Return top 3 ranked VendorRecommendation objects with:
- vendor_id, vendor_name
- score (0.0-1.0)
- estimated_cost
- delivery_days
- confidence
- risk_flags (["delay-risk"] if delivery_days > 5)
```

**Tools**:
- `VendorRepository` (get_vendor_metrics, list_by_category)

**Injected Dependencies**:
- `VendorRepository` (in-memory or SQL)
- `LLMService` (optional, for structured ranking)

**Invocation**:
```python
vendors = await vendor_intel.execute(VendorQuery(
    category="Raw materials",
    quantity=100,
    budget=50000
))
# Returns: [VendorRecommendation(...), VendorRecommendation(...), VendorRecommendation(...)]
```

---

### 5. Crisis Agent
**File**: `app/agents/crisis_agent.py`

**Prompt**:
```
You are the Crisis Response specialist. Analyze a critical incident and propose recovery.

Incident: {event_type}
Severity: {severity} (1-5 scale)
Payload: {payload}

Analyze:
1. Classify severity 1-5 (1=minor, 5=catastrophic)
2. Quantify impact:
   - Daily loss (revenue/cost)
   - Employees affected
   - Products affected
   - Recovery timeline in days
3. For supplier crises, query Vendor Intelligence for alternatives
4. Recommend team activation:
   - Severity 1-2: operations
   - Severity 3-4: operations, compliance, finance
   - Severity 5: operations, compliance, finance, executive

Return CrisisRecommendation:
- action: describe recovery
- severity_level: 1-5
- impact_analysis: {daily_loss, employees, products}
- recovery_timeline_days
- teams_to_activate: list
- confidence: 0.9 if daily_loss quantified, else lower

Do NOT execute recovery. Only propose.
```

**Tools**:
- `VendorIntelligenceAgent` (dependency, for supplier alternatives)
- `ProductRepository` (get products by supplier/factory)
- `IncidentRepository` (get employees affected)

**Injected Dependencies**:
- `VendorIntelligence` agent
- `ProductRepository`
- `IncidentRepository`
- `LLMService` (optional)

**Invocation**:
```python
crisis = await crisis_agent.execute(BusinessEventInput(
    event_type="VendorBankruptcy",
    severity="critical",
    payload={"vendor_id": "v-001", "daily_loss": 2300000, "employees_affected": 500}
))
# Calls: await self.dependencies[0].execute(VendorQuery(...)) for alternatives
# Returns: CrisisRecommendation(severity_level=5, teams_to_activate=["operations", "finance", "executive"], ...)
```

---

### 6. Finance Agent
**File**: `app/agents/finance_agent.py`

**Prompt**:
```
You are the Finance specialist. Validate spending and identify escalation requirements.

Event: {event_type}
Recommended Cost: {recommended_cost}
Available Budget: {available_budget}
Department: {department}
Recurring: {is_recurring}

Steps:
1. Check available budget >= recommended cost
   - If not, reject with "Exceeds available budget"
2. Calculate annualized cost (if recurring, multiply by 12)
3. Check if cost or annualized cost > CFO approval threshold ($100K)
   - If yes, escalate to CFO
4. Return FinanceDecision:
   - status: "approved" | "rejected" | "escalated"
   - available_budget
   - estimated_cost
   - annualized_cost
   - approval_role (if escalated)
```

**Tools**:
- `BudgetRepository` (department_budget, spending_to_date)

**Injected Dependencies**:
- `BudgetRepository` (in-memory or SQL)

**Invocation**:
```python
finance_dec = await finance.execute(RecommendationInput(
    event=event,
    recommendation=Recommendation(...),
    available_budget=150000
))
# Queries: await self.repository.department_budget("Procurement")
# Returns: FinanceDecision(status="escalated", approval_role="CFO", ...)
```

---

### 7. Compliance Agent
**File**: `app/agents/compliance_agent.py`

**Prompt**:
```
You are the Compliance specialist. Check vendor, spending, safety, and regulatory controls.

Event: {event_type}
Vendor: {vendor_id} (status: {vendor_status})
Spend: {spend_amount}
Recurring: {is_recurring}
Payload: {payload}

Deterministic checks (do NOT call LLM):
1. Vendor blacklist: Check if vendor_status in ["banned", "blacklisted"] → reject
2. Vendor audit hold: Check if vendor_status in ["audit", "under_audit"] → escalate
3. Export control: Check if payload.export_restricted → reject
4. Safety review: Check if payload.safety_critical and NOT payload.safety_reviewed → reject
5. Policy rules: Query PolicyRepository for active rules matching event type

Return ComplianceDecision:
- status: "compliant" | "non_compliant" | "escalated"
- violated_rules: list of rule IDs that matched
- controls_checked: list of all 10 controls evaluated
- reasoning: explain violations
```

**Tools**:
- `PolicyRepository` (active policies, rule matching)

**Injected Dependencies**:
- `PolicyRepository` (in-memory or SQL)

**Invocation**:
```python
compliance_dec = await compliance.execute(RecommendationInput(
    event=event,
    recommendation=Recommendation(...)
))
# Checks: vendor status, export restrictions, safety reviews
# Queries: await self.repository.active()
# Returns: ComplianceDecision(status="non_compliant", violated_rules=["POL-02", "POL-06"], ...)
```

---

### 8. Operations Agent
**File**: `app/agents/operations_agent.py`

**Prompt**:
```
You are the Operations specialist. Recommend operational remediation.

Event: {event_type}
Severity: {severity}
Payload: {payload}

Assess:
1. What is the operational impact? (downtime, lost capacity, etc.)
2. Who owns remediation? (operations manager, department head)
3. What constraints exist? (skill, equipment, time)
4. Recovery actions: (assign team, schedule maintenance, coordinate with other departments)

Return Recommendation:
- action: "Assign operations response team"
- rationale: explain constraints and owner
- confidence: 0.8-0.9 (high, deterministic)
- metadata: {owner: "operations", estimated_resolution_hours: 4}
```

**Tools**: None

**Injected Dependencies**: None

**Invocation**:
```python
ops_rec = await operations.execute(BusinessEventInput(...))
# Returns: Recommendation(action="Assign ops team", confidence=0.82, metadata={owner: "operations"})
```

---

### 9. Audit Agent
**File**: `app/agents/audit_agent.py`

**Prompt**:
```
You are the Audit specialist. Record immutable evidence of workflow transitions.

Event: {event_type}
Workflow State: {state_snapshot}
Actor: {current_user}
Transition: {from_step} → {to_step}
Decision: {decision_made}
Confidence: {confidence_score}
Latency: {latency_ms}
Tokens: {tokens_used}

Record:
- Actor (who triggered the transition)
- Transition (from → to)
- Inputs (what was passed to this step)
- Outputs (what was returned)
- Confidence (of recommending agent, if applicable)
- Latency (milliseconds to execute)
- Tokens (LLM tokens used, if applicable)
- Approval state (pending, approved, rejected)
- State snapshot (full workflow state at this point)

Do NOT mutate business state. Only log.

Return audit dict:
- audited: true
- event_type: {event_type}
- snapshots: [...] (list of state snapshots)
```

**Tools**:
- `AuditService` (record method, injected)

**Injected Dependencies**:
- `AuditService`

**Invocation**:
```python
audit_result = await audit.execute(BusinessEventInput(...))
# Records to AuditLog table
# Returns: {audited: True, event_type: "VendorBankruptcy", snapshots: [...]}
```

---

### 10. Notification Agent
**File**: `app/agents/notification_agent.py`

**Prompt**:
```
You are the Notification specialist. Route notifications to stakeholders.

Event: {event_type}
Severity: {severity}
Recipient Roles: {recipient_roles}
Notification Channels: {channels}

Routes:
- Severity "critical" → Email + Slack + SMS (urgent)
- Severity "high" → Email + Slack
- Severity "medium" → Email
- Severity "low" → Log only

For each channel:
1. Select recipient by role (CEO, Finance, Operations, etc.)
2. Compose subject and body
3. Attempt delivery (retry 3x on transient errors)
4. Log delivery status

Do NOT approve or execute. Only notify.

Return delivery dict:
- queued: bool (all channels queued?)
- channels: [{channel: "email", recipient: "...", delivered: bool, error: null|str}, ...]
- audience_roles: list (who was notified)
```

**Tools**:
- `NotificationService` (send via Email/Slack/SMS)

**Injected Dependencies**:
- `NotificationService`

**Invocation**:
```python
notif_result = await notification.execute(BusinessEventInput(...))
# Calls: await self.service.send("email", recipient, subject, body)
# Retries on TimeoutError/ConnectionError
# Returns: {queued: True, channels: [{channel: "email", delivered: True, ...}], ...}
```

---

## Skills (Reusable Agent Behaviors)

Skills are composable behaviors that multiple agents can use. They live in `app/agents/skills/`.

### Skill: Vendor Scoring
**File**: `app/agents/skills/vendor_scoring.py`

```python
async def score_vendors(
    candidates: list[dict],
    weights: dict = {"delivery": 0.8, "cost": 0.1, "risk": 0.1}
) -> list[VendorRecommendation]:
    """
    Generic vendor scoring skill used by:
    - VendorIntelligenceAgent
    - ProcurementAgent
    - CrisisAgent (for alternatives)
    """
    results = []
    for candidate in candidates:
        score = (
            weights["delivery"] * candidate["on_time_rate"] +
            weights["cost"] * candidate["cost_competitiveness"] +
            weights["risk"] * (1 - candidate["risk_rate"])
        )
        results.append(VendorRecommendation(
            vendor_id=candidate["id"],
            vendor_name=candidate["name"],
            score=score,
            ...
        ))
    return sorted(results, key=lambda x: x.score, reverse=True)[:3]
```

### Skill: Risk Flag Generation
**File**: `app/agents/skills/risk_flagging.py`

```python
def generate_risk_flags(
    event: BusinessEventInput,
    recommendation: Recommendation
) -> list[str]:
    """
    Generic risk flag skill used by:
    - ProcurementAgent
    - CrisisAgent
    - VendorIntelligenceAgent
    """
    flags = []
    
    if event.payload.get("budget", 0) <= 0:
        flags.append("budget-missing")
    
    if "delay" in event.event_type.lower():
        flags.append("supplier-continuity")
    
    if recommendation.estimated_cost > 50000:
        flags.append("high-spend")
    
    return flags
```

### Skill: Impact Quantification
**File**: `app/agents/skills/impact_analysis.py`

```python
def quantify_impact(
    event: BusinessEventInput,
    scenario: str = "worst-case"
) -> dict:
    """
    Quantify business impact from payload signals.
    Used by: CrisisAgent, IncidentRepository lookup
    """
    p = event.payload
    
    daily_loss = float(p.get("daily_loss", p.get("revenue_at_risk", 0)) or 0)
    employees = int(p.get("employees_affected", 0) or 0)
    products = p.get("products_affected", []) or []
    
    if scenario == "worst-case":
        daily_loss *= 1.5  # 50% escalation multiplier
    
    return {
        "daily_loss": daily_loss,
        "employees_affected": employees,
        "products_affected": products,
        "recovery_days": max(1, int(daily_loss / 500000)),  # Rough heuristic
    }
```

---

## Dependency Injection Pattern

All agents accept injected dependencies in `__init__`:

```python
class ProcurementAgent(Agent[BusinessEventInput, Recommendation]):
    def __init__(
        self,
        vendor_intelligence: VendorIntelligenceAgent | None = None,
        llm_service: LLMService | None = None
    ):
        self.vendor_agent = vendor_intelligence or VendorIntelligenceAgent()
        self.llm = llm_service or LLMService()
```

**Orchestrator Initialization** (`app/agents/orchestrator.py`):
```python
class AgentOrchestrator:
    def __init__(self, llm_service: LLMService | None = None):
        llm = llm_service or LLMService()
        vendor = VendorIntelligenceAgent(llm_service=llm)
        
        self.agents = {
            "planner": PlannerAgent(),
            "coo": COOAgent(),
            "procurement": ProcurementAgent(vendor_agent=vendor, llm_service=llm),
            "crisis": CrisisAgent(vendor_agent=vendor, llm_service=llm),
            "finance": FinanceAgent(),
            "compliance": ComplianceAgent(),
            "operations": OperationsAgent(),
            "vendor_intelligence": vendor,
            "audit": AuditAgent(),
            "notification": NotificationAgent(),
        }
```

---

## LLM Provider Integration

Each agent that calls LLM uses `LLMService`:

```python
from app.services.llm import LLMService

class CrisisAgent(Agent):
    def __init__(self, llm_service: LLMService | None = None):
        self.llm = llm_service or LLMService()
    
    async def run(self, value: BusinessEventInput) -> CrisisRecommendation:
        if self.llm:
            try:
                plan, response = await self.llm.call_structured(
                    f"Create crisis recovery plan for {event_type}...",
                    CrisisRecommendation
                )
                return plan
            except RuntimeError:
                # Fallback to deterministic defaults
                return self._baseline_recommendation()
```

**Provider Fallback**:
1. Gemini (primary) → 0s cost, fast reasoning
2. Groq (secondary) → Latency-optimized
3. OpenRouter (tertiary) → Cost-optimized

If all fail or no keys configured, agents use **repository-backed defaults** (in-memory mock data).

---

## Repository Injection

Policy, budget, vendor, incident repositories are injected:

```python
class FinanceAgent(Agent):
    def __init__(self, repository: BudgetRepository | None = None):
        self.repository = repository or InMemoryBudgetRepository()

class ComplianceAgent(Agent):
    def __init__(self, repository: PolicyRepository | None = None):
        self.repository = repository or InMemoryPolicyRepository()
```

**For SQL at runtime**:
```python
from app.repositories.vendor_repository import SQLAlchemyVendorRepository

vendor_repo = SQLAlchemyVendorRepository(db_session)
vendor_agent = VendorIntelligenceAgent(repository=vendor_repo)
```

---

## Notification Channel Adaptation

Custom notification channels are injected:

```python
from app.notifications.service import NotificationService, Channel

class SlackChannel(Channel):
    name = "slack"
    async def send(self, recipient: str, subject: str, body: str) -> None:
        # POST to Slack webhook
        pass

class EmailChannel(Channel):
    name = "email"
    async def send(self, recipient: str, subject: str, body: str) -> None:
        # POST to Resend API
        pass

notif_service = NotificationService(channels={
    "email": EmailChannel(),
    "slack": SlackChannel()
})

notif_agent = NotificationAgent(service=notif_service)
```

---

## Testing Patterns

### Unit Test with Mock Repositories
```python
@pytest.mark.asyncio
async def test_finance_agent_rejects_overspend():
    budget_repo = InMemoryBudgetRepository(
        budgets={"Procurement": 50000},
        spending={"Procurement,current_fiscal_year": 40000}
    )
    agent = FinanceAgent(repository=budget_repo)
    
    result = await agent.execute(RecommendationInput(
        event=event,
        recommendation=Recommendation(estimated_cost=15000)
    ))
    
    assert result.status == "rejected"
    assert result.available_budget == 10000
```

### Integration Test with Real DB
```python
@pytest.mark.asyncio
async def test_vendor_ranking_e2e(db_session):
    vendor_repo = SQLAlchemyVendorRepository(db_session)
    agent = VendorIntelligenceAgent(repository=vendor_repo)
    
    result = await agent.execute(VendorQuery(
        category="Raw materials",
        budget=50000
    ))
    
    assert len(result) == 3
    assert result[0].score >= result[1].score >= result[2].score
```

---

## Configuration

Environment variables for agent behavior:

```bash
# app/config/settings.py
AGENT_TIMEOUT_SECONDS=30
AGENT_CONFIDENCE_THRESHOLD=0.7
LLM_FALLBACK_TO_DEFAULTS=true
LLM_STRUCTURED_OUTPUT_RETRIES=2

GEMINI_API_KEY=...
GROQ_API_KEY=...
OPENROUTER_API_KEY=...

RESEND_API_KEY=...
SLACK_BOT_TOKEN=...
```

---

## Summary Table

| Agent | Input | Output | LLM | Repos | Skills | Timeout |
|-------|-------|--------|-----|-------|--------|---------|
| Planner | Event | Plan | ❌ | ❌ | ❌ | 30s |
| COO | Event+Plan+Policy | Routing | ❌ | ❌ | ❌ | 30s |
| Procurement | Event | Recommendation | ✅ | ❌ | Vendor Scoring | 30s |
| VendorIntel | VendorQuery | RankedVendors | ✅ | VendorRepo | Vendor Scoring | 30s |
| Crisis | Event | CrisisRec | ✅ | Product, Incident | Impact Analysis | 30s |
| Finance | Event+Rec | FinanceDecision | ❌ | BudgetRepo | ❌ | 30s |
| Compliance | Event+Rec | ComplianceDecision | ❌ | PolicyRepo | Risk Flagging | 30s |
| Operations | Event | Recommendation | ❌ | ❌ | ❌ | 30s |
| Audit | Event | AuditDict | ❌ | ❌ | ❌ | 30s |
| Notification | Event | DeliveryDict | ❌ | ❌ | ❌ | 30s |

---

**Last Updated**: Hackathon submission (Deploy or Die 2026)