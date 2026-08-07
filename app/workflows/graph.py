from typing import Any, Literal, TypedDict
from app.agents.orchestrator import AgentOrchestrator
from app.schemas.agents import BusinessEventInput
from app.services.policy import PolicyEngine

class WorkflowState(TypedDict, total=False):
    workflow_id: str; event: dict[str, Any]; status: str; plan: dict[str, Any]; policy: dict[str, Any]; recommendations: dict[str, Any]; approval: dict[str, Any]; execution: dict[str, Any]; audit: list[dict[str, Any]]; error: str

class WorkflowOrchestrator:
    """LangGraph master graph: classifier -> planner -> policy -> specialists -> approval interrupt -> execute -> audit."""
    def __init__(self, policy_engine=None, agents=None): self.policy=policy_engine or PolicyEngine(); self.agents=agents or AgentOrchestrator()
    def build(self, checkpointer=None):
        from langgraph.graph import END, START, StateGraph
        from langgraph.types import interrupt
        async def classify(state): return {"status":"classified","audit":[*state.get("audit",[]),{"action":"classified"}]}
        async def plan(state):
            event=BusinessEventInput.model_validate(state["event"]); result=await self.agents.get("planner").execute({**event.model_dump(),"policy":None}); return {"status":"planning","plan":result.model_dump()}
        async def policy(state):
            decision=self.policy.evaluate(state["event"],state.get("recommendations",{})); return {"status":"policy_check","policy":decision.model_dump()}
        async def specialists(state):
            event=BusinessEventInput.model_validate(state["event"]); name="crisis" if event.event_type.lower() in {"factoryfire","cyberattack","supplierbankruptcy","poweroutage","machinefailure","vendorbankruptcy"} else "procurement" if event.event_type.lower() in {"purchaserequest","vendordelay"} else "operations"; result=await self.agents.get(name).execute(event); return {"status":"awaiting_approval","recommendations":{name:result.model_dump() if hasattr(result,"model_dump") else result}}
        async def approval(state):
            decision=interrupt({"workflow_id":state.get("workflow_id"),"action":"approve_recommendation","context":state.get("recommendations",{}),"expires_minutes":30}); return {"status":"approved" if decision.get("decision")=="approved" else "rejected","approval":decision}
        async def execute(state): return {"status":"executing","execution":{"executed":True,"critical_action":"delegated_to_external_executor"}}
        async def audit(state): return {"status":"completed","audit":[*state.get("audit",[]),{"action":"completed","snapshot":dict(state)}]}
        def route_policy(state)->Literal["reject","specialists"]: return "reject" if state.get("policy",{}).get("status")=="rejected" else "specialists"
        def route_approval(state)->Literal["execute","reject"]: return "execute" if state.get("status")=="approved" else "reject"
        graph=StateGraph(WorkflowState); graph.add_node("classify",classify); graph.add_node("planner",plan); graph.add_node("policy",policy); graph.add_node("specialists",specialists); graph.add_node("approval",approval); graph.add_node("execute",execute); graph.add_node("audit",audit)
        graph.add_edge(START,"classify"); graph.add_edge("classify","planner"); graph.add_edge("planner","policy"); graph.add_conditional_edges("policy",route_policy,{"reject":"audit","specialists":"specialists"}); graph.add_edge("specialists","approval"); graph.add_conditional_edges("approval",route_approval,{"execute":"execute","reject":"audit"}); graph.add_edge("execute","audit"); graph.add_edge("audit",END)
        return graph.compile(checkpointer=checkpointer)
