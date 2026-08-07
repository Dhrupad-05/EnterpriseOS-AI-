from app.agents.contract import Agent
from app.schemas.agents import BusinessEventInput
class AuditAgent(Agent[BusinessEventInput, dict]):
    name="audit"; description="Captures immutable workflow transition evidence and replay snapshots."; input_schema=BusinessEventInput; output_schema=dict
    instructions="Record actor, transition, inputs, outputs, confidence, latency, tokens, approval state, and state snapshot. Never mutate business state."
    async def run(self,value): return {"audited":True,"event_type":value.event_type}
