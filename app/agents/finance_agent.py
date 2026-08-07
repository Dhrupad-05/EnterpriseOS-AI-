from app.agents.contract import Agent
from app.schemas.agents import FinanceDecision, RecommendationInput
from app.repositories.budget_repository import InMemoryBudgetRepository
class FinanceAgent(Agent[RecommendationInput, FinanceDecision]):
    name="finance"; description="Validates funding, annualized cost, currency, and CFO escalation."; input_schema=RecommendationInput; output_schema=FinanceDecision
    instructions="Check available funds, normalize currency, calculate recurring 12-month impact, and escalate material spend. Never release funds."
    def __init__(self, repository=None): self.repository=repository or InMemoryBudgetRepository()
    async def run(self,value):
        r=value.recommendation; p=value.event.payload; cost=float(r.estimated_cost if r else p.get("cost",p.get("amount",0)) or 0); recurring=bool(p.get("recurring",p.get("is_recurring",False))); annual=cost*12 if recurring else cost; threshold=float(p.get("cfo_threshold",100000)); department=p.get("department")
        configured_budget=await self.repository.department_budget(department) if department else 0; spent=await self.repository.spending_to_date(department,"current_fiscal_year") if department else 0; available=value.available_budget or max(configured_budget-spent,0)
        if cost>available: return FinanceDecision(status="rejected",reasoning="Requested cost exceeds available budget.",available_budget=available,estimated_cost=cost,annualized_cost=annual,currency=value.currency)
        if cost>threshold or annual>threshold: return FinanceDecision(status="escalated",reasoning="Spend exceeds CFO approval threshold.",available_budget=available,estimated_cost=cost,annualized_cost=annual,currency=value.currency,approval_role="CFO")
        return FinanceDecision(status="approved",reasoning="Cost is within available budget and delegated threshold.",available_budget=available,estimated_cost=cost,annualized_cost=annual,currency=value.currency)
