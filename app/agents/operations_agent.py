from app.agents.contract import Agent
from app.schemas.agents import BusinessEventInput, Recommendation
class OperationsAgent(Agent[BusinessEventInput, Recommendation]):
    name="operations"; description="Recommends operational remediation actions."; input_schema=BusinessEventInput; output_schema=Recommendation
    instructions="Assess operational constraints, dependencies, owners, and recovery actions; recommend only."
    async def run(self,value): return Recommendation(action="Assign operations response team",rationale="Operational owner required for event remediation.",confidence=.82,metadata={"owner":"operations"})
