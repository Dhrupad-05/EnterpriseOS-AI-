# Agent development contract

Agents recommend; policy governs; humans approve; executors perform. Every agent is a typed `Agent[InputModel, OutputModel]` with a unique name, description, reasoning instructions, confidence threshold, 30-second hard timeout, retry policy, and explicit dependency list.

| Agent | Contract | Default confidence | Key scenarios |
|---|---|---:|---|
| Planner | Event → ExecutionPlan | 0.70 | decomposes work, gates, dependencies |
| COO | Event + Plan + Policy → routing | 0.70 | parallel/sequential specialist routing |
| Procurement | Event → Recommendation | 0.70 | budget, urgency, alternatives |
| Vendor Intelligence | VendorQuery → ranked vendors | 0.50 | delivery/cost/risk scoring |
| Crisis | Crisis Event → CrisisRecommendation | 0.70 | impact, continuity, resource activation |
| Finance | RecommendationInput → FinanceDecision | 0.70 | budget, recurring cost, CFO escalation |
| Compliance | RecommendationInput → ComplianceDecision | 0.70 | blacklist, safety, export, approvals |
| Audit | Event → immutable evidence | 0.70 | transitions, snapshots, replay |
| Notification | Event → delivery plan | 0.70 | role-aware email/Slack/SMS/push |

Dependencies are a DAG. No agent owns payment, procurement, notification, or other critical side effects. Those actions are commands emitted only after PolicyEngine approval and human approval.
