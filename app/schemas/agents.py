from typing import Any, Literal
from pydantic import BaseModel, Field, ConfigDict

class BusinessEventInput(BaseModel):
    model_config = ConfigDict(extra="allow")
    event_type: str = Field(min_length=1)
    title: str
    description: str
    severity: str = "medium"
    payload: dict[str, Any] = Field(default_factory=dict)

class VendorRecommendation(BaseModel):
    vendor_id: str
    vendor_name: str
    score: float = Field(ge=0, le=1)
    estimated_cost: float = Field(ge=0)
    delivery_days: int = Field(ge=0)
    confidence: float = Field(ge=0, le=1)
    risk_flags: list[str] = Field(default_factory=list)
    reasoning: str = ""
class VendorRankingOutput(BaseModel):
    primary_vendor: VendorRecommendation
    alternatives: list[VendorRecommendation] = Field(default_factory=list)
    recommendation: str
    total_cost_estimate: float = 0
    implementation_timeline_days: int = 0

class VendorQuery(BaseModel):
    category: str
    quantity: int = Field(default=1, ge=1)
    urgency: str = "standard"
    budget: float = Field(default=0, ge=0)
    candidates: list[dict[str, Any]] = Field(default_factory=list)

class Recommendation(BaseModel):
    action: str
    rationale: str
    confidence: float = Field(ge=0, le=1)
    estimated_cost: float = Field(default=0, ge=0)
    alternatives: list[VendorRecommendation] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class RecommendationInput(BaseModel):
    event: BusinessEventInput
    recommendation: Recommendation | None = None
    available_budget: float = Field(default=0, ge=0)
    currency: str = "USD"

class CrisisRecommendation(Recommendation):
    severity_level: int = Field(ge=1, le=5)
    impact_analysis: dict[str, Any] = Field(default_factory=dict)
    recovery_timeline_days: int = Field(ge=0)
    teams_to_activate: list[str] = Field(default_factory=list)

class FinanceDecision(BaseModel):
    status: Literal["approved", "rejected", "escalated"]
    reasoning: str
    available_budget: float = Field(ge=0)
    estimated_cost: float = Field(ge=0)
    annualized_cost: float = Field(ge=0)
    currency: str = "USD"
    approval_role: str | None = None

class ComplianceDecision(BaseModel):
    status: Literal["compliant", "non_compliant", "escalated"]
    reasoning: str
    violated_rules: list[str] = Field(default_factory=list)
    controls_checked: list[str] = Field(default_factory=list)

class PlanStep(BaseModel):
    order: int
    name: str
    owner: str
    duration_minutes: int = Field(ge=1)
    requires_approval: bool = False
    dependencies: list[int] = Field(default_factory=list)

class ExecutionPlan(BaseModel):
    steps: list[PlanStep]
    estimated_duration_minutes: int = Field(ge=1)
    approval_gates: list[str] = Field(default_factory=list)
    parallel_groups: list[list[int]] = Field(default_factory=list)

class PolicyDecision(BaseModel):
    status: Literal["approved", "rejected", "escalated"]
    reason: str
    matched_rules: list[str] = Field(default_factory=list)
    required_approval_role: str | None = None
    requires_approval: bool = True
    @property
    def permitted(self) -> bool:
        return self.status != "rejected"
