from dataclasses import dataclass, field
from typing import Any, Callable
from app.schemas.agents import PolicyDecision

@dataclass(frozen=True)
class BusinessRule:
    rule_id: str
    name: str
    priority: int
    matcher: Callable[[dict[str, Any], dict[str, Any]], bool]
    evaluator: Callable[[dict[str, Any], dict[str, Any]], tuple[str, str | None, str | None]]

@dataclass
class PolicyResult:
    permitted: bool
    requires_approval: bool
    reasons: list[str] = field(default_factory=list)
    escalation: str | None = None
    status: str = "approved"
    matched_rules: list[str] = field(default_factory=list)

class PolicyEngine:
    """Deterministic governance boundary. Rules are data-backed in production and versioned."""
    def __init__(self, rules: list[BusinessRule] | None = None): self.rules=sorted(rules or self.default_rules(),key=lambda r:r.priority)
    @staticmethod
    def default_rules():
        return [
            BusinessRule("BUDGET-50K","Purchases above $50K require Finance approval",10,lambda e,r: float(e.get("payload",{}).get("amount",0) or 0)>50000,lambda e,r:("escalated",None,"Finance")),
            BusinessRule("VENDOR-BLACKLIST","Blacklisted vendors are prohibited",20,lambda e,r: str(e.get("payload",{}).get("vendor_status","")).lower() in {"banned","blacklisted"},lambda e,r:("rejected","Vendor is prohibited by policy",None)),
            BusinessRule("CRISIS-CEO","Crisis severity above 3 requires CEO notification",30,lambda e,r: int(e.get("payload",{}).get("severity_level",0) or 0)>3,lambda e,r:("escalated",None,"CEO")),
            BusinessRule("REFUND-MANAGER","Refunds above $1K require manager approval",40,lambda e,r: e.get("event_type","").lower()=="customerrefund" and float(e.get("payload",{}).get("amount",0) or 0)>1000,lambda e,r:("escalated",None,"Manager")),
            BusinessRule("INVENTORY-REORDER","Inventory below 10% triggers reorder",50,lambda e,r: float(e.get("payload",{}).get("inventory_ratio",1) or 1)<.1,lambda e,r:("escalated",None,"Operations")),
        ]
    def evaluate(self,event: dict[str,Any],recommendations: dict[str,Any]|None=None)->PolicyDecision:
        matched=[]; escalations=[]
        if isinstance(recommendations, list):
            for item in recommendations:
                rules=item.get("rules",{}) if isinstance(item,dict) else {}
                limit=rules.get("budget_limit")
                amount=float(event.get("payload",{}).get("amount",0) or 0)
                if limit is not None and amount>float(limit):
                    return PolicyDecision(status="rejected",reason=f"budget limit exceeded by {item.get('name','policy')}",matched_rules=[str(item.get("name","policy"))],requires_approval=True)
                if rules.get("approval_required"): escalations.append(rules.get("escalation_role","Manager"))
        for rule in self.rules:
            if rule.matcher(event,recommendations or {}):
                matched.append(rule.rule_id); status,reason,role=rule.evaluator(event,recommendations or {})
                if status=="rejected": return PolicyDecision(status="rejected",reason=reason or rule.name,matched_rules=matched,required_approval_role=None,requires_approval=False)
                if role: escalations.append(role)
        if event.get("severity") in {"high","critical"}: matched.append("IMPACT-APPROVAL"); escalations.append("Manager")
        role=escalations[-1] if escalations else None
        return PolicyDecision(status="escalated" if role else "approved",reason="; ".join(matched) if matched else "No restrictive rules matched",matched_rules=matched,required_approval_role=role,requires_approval=True)
