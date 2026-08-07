from app.agents.crisis_agent import CrisisAgent
from app.agents.finance_agent import FinanceAgent
from app.agents.compliance_agent import ComplianceAgent
from app.schemas.agents import BusinessEventInput, Recommendation, RecommendationInput
async def test_crisis_cascading_impact():
    r=await CrisisAgent().execute(BusinessEventInput(event_type="FactoryFire",title="fire",description="fire",severity="critical",payload={"daily_loss":2300000,"employees_affected":500}))
    assert r.severity_level==5 and r.impact_analysis["employees_affected"]==500
async def test_finance_escalates_cfo():
    r=await FinanceAgent().execute(RecommendationInput(event=BusinessEventInput(event_type="PurchaseRequest",title="x",description="y"),recommendation=Recommendation(action="x",rationale="y",confidence=.9,estimated_cost=100001),available_budget=200000))
    assert r.status=="escalated" and r.approval_role=="CFO"
async def test_compliance_blacklist():
    r=await ComplianceAgent().execute(RecommendationInput(event=BusinessEventInput(event_type="PurchaseRequest",title="x",description="y",payload={"vendor_status":"blacklisted"})))
    assert r.status=="non_compliant" and "POL-02" in r.violated_rules[0]
