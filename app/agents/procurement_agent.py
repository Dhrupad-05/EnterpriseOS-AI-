from app.agents.contract import Agent
from app.agents.vendor_intelligence_agent import VendorIntelligenceAgent
from app.schemas.agents import BusinessEventInput, Recommendation, VendorQuery

class ProcurementAgent(Agent[BusinessEventInput, Recommendation]):
    name = "procurement"
    description = "Builds procurement recommendations with ranked vendors and fallbacks."
    input_schema = BusinessEventInput
    output_schema = Recommendation
    instructions = "Analyze quantity, urgency, budget, vendor alternatives, delivery risk, and approval implications. Recommend only; never place an order."
    dependencies = [VendorIntelligenceAgent()]
    async def run(self, value: BusinessEventInput) -> Recommendation:
        payload = value.payload
        budget = float(payload.get("budget", payload.get("amount", 0)) or 0)
        quantity = int(payload.get("quantity", 1) or 1)
        vendors = await self.dependencies[0].execute(VendorQuery(category=payload.get("category", "general"), quantity=quantity, urgency=payload.get("urgency", "standard"), budget=budget))
        risks = ["budget-missing"] if budget <= 0 else []
        if value.event_type.lower() == "vendordelay": risks.append("supplier-continuity")
        lead = vendors[0].delivery_days if vendors else 0
        return Recommendation(action=f"Request quote from {vendors[0].vendor_name}" if vendors else "Escalate vendor search", rationale="Ranked by delivery performance, cost, and risk.", confidence=vendors[0].confidence if vendors else .3, estimated_cost=vendors[0].estimated_cost if vendors else 0, alternatives=vendors, risk_flags=risks, metadata={"quantity": quantity, "urgency": payload.get("urgency", "standard"), "lead_days": lead})
