from app.agents.contract import Agent
from app.agents.vendor_intelligence_agent import VendorIntelligenceAgent
from app.schemas.agents import BusinessEventInput, CrisisRecommendation, VendorQuery
from app.repositories.incident_repository import InMemoryIncidentRepository
from app.repositories.product_repository import InMemoryProductRepository
class CrisisAgent(Agent[BusinessEventInput, CrisisRecommendation]):
    name="crisis"; description="Analyzes crisis impact, continuity, recovery, and resource activation."; input_schema=BusinessEventInput; output_schema=CrisisRecommendation
    instructions="Classify severity 1-5, quantify impact, identify recovery options, activate the right teams, and expose loss assumptions. Never execute."
    dependencies=[VendorIntelligenceAgent()]
    def __init__(self, product_repository=None, incident_repository=None, vendor_agent=None, llm_service=None):
        self.product_repository=product_repository or InMemoryProductRepository(); self.incident_repository=incident_repository or InMemoryIncidentRepository(); self.dependencies=[vendor_agent or VendorIntelligenceAgent()]; self.llm=llm_service
    async def run(self,value):
        p=value.payload; event=value.event_type.lower(); crisis_type=str(p.get("type",value.event_type)).upper(); severity=int(p.get("severity_level",5 if value.severity=="critical" else 4 if value.severity=="high" else 3)); employees=await self.incident_repository.employees_affected(crisis_type,p)
        products=await self.product_repository.by_supplier(str(p.get("vendor_id"))) if "bankruptcy" in event or "supplier" in event else await self.product_repository.by_factory(str(p.get("factory_id"))) if "fire" in event else []
        daily_loss=float(p.get("daily_loss",p.get("revenue_at_risk",max(len(products),1)*float(p.get("revenue_per_product",50000)))) or 0)
        alternatives=[]
        if any(x in event for x in ("bankruptcy","delay","supplier")): alternatives=await self.dependencies[0].execute(VendorQuery(category=p.get("category","critical supply"),budget=float(p.get("recovery_budget",0) or 0)))
        teams=["operations","compliance","finance","executive"] if severity>=4 else ["operations"]
        baseline=CrisisRecommendation(action="Activate crisis continuity plan",rationale=f"{crisis_type}: severity {severity}/5; estimated exposure ${daily_loss:,.0f}/day.",confidence=.9 if daily_loss else .72,estimated_cost=float(p.get("recovery_cost",0) or 0),alternatives=alternatives,risk_flags=["employee-safety"] if employees else [],severity_level=max(1,min(5,severity)),impact_analysis={"daily_loss":daily_loss,"employees_affected":employees,"products_affected":p.get("products_affected",[]) or [x.get("name") for x in products]},recovery_timeline_days=int(p.get("recovery_days",2 if severity>=4 else 5)),teams_to_activate=teams)
        if self.llm:
            try:
                plan,_=await self.llm.call_structured(f"Create a conservative crisis recovery recommendation for {crisis_type}. Preserve severity {severity}, daily loss {daily_loss}, employees {employees}, and these supplier alternatives: {[x.model_dump() for x in alternatives]}",CrisisRecommendation)
                return plan
            except RuntimeError:
                pass
        return baseline
