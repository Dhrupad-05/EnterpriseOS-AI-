from app.agents.contract import Agent
from app.schemas.agents import BusinessEventInput, ExecutionPlan, PolicyDecision
class COOInput(BusinessEventInput):
    plan: ExecutionPlan | None = None
    policy: PolicyDecision | None = None
class COOAgent(Agent[COOInput, dict]):
    name="coo"; description="Coordinates specialists and graph routing; never executes actions."; input_schema=COOInput; output_schema=dict
    instructions="Select specialist agents, honor dependencies and parallelism, aggregate recommendations, and stop at approval. No side effects."
    async def run(self,value):
        event=value.event_type.lower(); specialists=["crisis"] if event in {"factoryfire","cyberattack","supplierbankruptcy","poweroutage","machinefailure","vendorbankruptcy"} else ["procurement"] if event in {"purchaserequest","vendordelay"} else ["operations"]
        specialists += ["finance","compliance"]
        return {"specialist_agents":specialists,"can_execute":False,"approval_gate_required":True,"parallel":specialists[1:]}
