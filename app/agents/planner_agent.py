from app.agents.contract import Agent
from app.schemas.agents import BusinessEventInput, ExecutionPlan, PlanStep, PolicyDecision
class PlannerInput(BusinessEventInput):
    policy: PolicyDecision | None = None
class PlannerAgent(Agent[PlannerInput, ExecutionPlan]):
    name="planner"; description="Decomposes an event into timed, governed steps."; input_schema=PlannerInput; output_schema=ExecutionPlan
    instructions="Decompose into explicit work, resource owners, dependencies, parallel groups, duration, and approval gates. Do not execute."
    async def run(self,value):
        crisis=value.event_type.lower() in {"factoryfire","cyberattack","supplierbankruptcy","poweroutage","machinefailure","vendorbankruptcy"}
        steps=[PlanStep(order=1,name="classify_event",owner="coo",duration_minutes=1),PlanStep(order=2,name="analyze_impact" if crisis else "prepare_recommendation",owner="crisis" if crisis else "specialist",duration_minutes=5),PlanStep(order=3,name="policy_check",owner="policy",duration_minutes=1),PlanStep(order=4,name="human_approval",owner="approval_queue",duration_minutes=30,requires_approval=True),PlanStep(order=5,name="execute_approved_actions",owner="executor",duration_minutes=10,dependencies=[4]),PlanStep(order=6,name="audit_and_notify",owner="audit",duration_minutes=2,dependencies=[5])]
        return ExecutionPlan(steps=steps,estimated_duration_minutes=sum(s.duration_minutes for s in steps),approval_gates=["human_approval"],parallel_groups=[[2,3]] if crisis else [])
