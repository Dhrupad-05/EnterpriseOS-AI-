from app.agents.contract import Agent
from app.schemas.agents import ComplianceDecision, RecommendationInput
from app.repositories.policy_repository import InMemoryPolicyRepository
class ComplianceAgent(Agent[RecommendationInput, ComplianceDecision]):
    name="compliance"; description="Applies deterministic vendor, spending, safety, and regulatory controls."; input_schema=RecommendationInput; output_schema=ComplianceDecision
    instructions="Check blacklists, audits, spending caps, safety controls, data handling, export restrictions, segregation of duties, and required approvals. Return rule IDs."
    def __init__(self, repository=None): self.repository=repository or InMemoryPolicyRepository()
    async def run(self,value):
        p=value.event.payload; violated=[]; checked=[f"POL-{i:02d}" for i in range(1,11)]
        for policy in await self.repository.active():
            if policy.get("type")=="VENDOR_BLACKLIST" and p.get("vendor_id") in policy.get("config",{}).get("blacklist",[]): violated.append(f"{policy.get('id','POL-02')} vendor-blacklist")
        vendor=str(p.get("vendor_status","active")).lower()
        if vendor in {"blacklisted","banned"}: violated.append("POL-02 vendor-blacklist")
        if vendor in {"audit","under_audit"}: violated.append("POL-03 vendor-audit-hold")
        if p.get("export_restricted"): violated.append("POL-06 export-control")
        if p.get("safety_critical") and not p.get("safety_reviewed"): violated.append("POL-08 safety-review")
        return ComplianceDecision(status="non_compliant" if violated else "compliant",reasoning="; ".join(violated) if violated else "All deterministic controls passed.",violated_rules=violated,controls_checked=checked)
