from app.agents.contract import Agent
from app.schemas.agents import FinanceDecision, RecommendationInput
class FinanceAgent(Agent[RecommendationInput, FinanceDecision]):
    name="finance"; description="Validates funding, annualized cost, currency, and CFO escalation."; input_schema=RecommendationInput; output_schema=FinanceDecision
    instructions="Check available funds, normalize currency, calculate recurring 12-month impact, and escalate material spend. Never release funds."
    async def run(self,value):
        r=value.recommendation; cost=float(r.estimated_cost if r else 0); recurring=bool(value.event.payload.get("recurring",False)); annual=cost*12 if recurring else cost; threshold=float(value.event.payload.get("cfo_threshold",100000));
        if cost>value.available_budget: return FinanceDecision(status="rejected",reasoning="Requested cost exceeds available budget.",available_budget=value.available_budget,estimated_cost=cost,annualized_cost=annual,currency=value.currency)
        if cost>threshold or annual>threshold: return FinanceDecision(status="escalated",reasoning="Spend exceeds CFO approval threshold.",available_budget=value.available_budget,estimated_cost=cost,annualized_cost=annual,currency=value.currency,approval_role="CFO")
        return FinanceDecision(status="approved",reasoning="Cost is within available budget and delegated threshold.",available_budget=value.available_budget,estimated_cost=cost,annualized_cost=annual,currency=value.currency)
