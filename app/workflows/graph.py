from typing import Any, Literal, TypedDict
from app.agents.orchestrator import AgentOrchestrator
from app.agents.coo_agent import COOInput
from app.schemas.agents import BusinessEventInput, RecommendationInput
from app.services.policy import PolicyEngine
from app.observability.prometheus import AGENT_EXECUTIONS, AGENT_LATENCY, WORKFLOWS

class WorkflowState(TypedDict, total=False):
    workflow_id: str; event: dict[str, Any]; status: str; plan: dict[str, Any]; policy: dict[str, Any]; recommendations: dict[str, Any]; approval: dict[str, Any]; execution: dict[str, Any]; audit: list[dict[str, Any]]; error: str

class WorkflowOrchestrator:
    """LangGraph master graph: classifier -> planner -> policy -> specialists -> approval interrupt -> execute -> audit."""
    def __init__(self, policy_engine=None, agents=None, snapshot_store=None): self.policy=policy_engine or PolicyEngine(); self.agents=agents or AgentOrchestrator(); self.snapshot_store=snapshot_store
    def build(self, checkpointer=None):
        from langgraph.graph import END, START, StateGraph
        from langgraph.types import interrupt
        async def persist(state,update):
            merged={**state,**update}
            if self.snapshot_store: await self.snapshot_store.save(state.get("workflow_id","unknown"),merged)
            return update
        async def classify(state): return await persist(state,{"status":"classified","audit":[*state.get("audit",[]),{"action":"classified"}]})
        async def plan(state):
            event=BusinessEventInput.model_validate(state["event"]); result=await self.agents.get("planner").execute({**event.model_dump(),"policy":None}); return await persist(state,{"status":"planning","plan":result.model_dump()})
        async def policy(state):
            decision=self.policy.evaluate(state["event"],state.get("recommendations",{})); return await persist(state,{"status":"policy_check","policy":decision.model_dump()})
        async def specialists(state):
            event=BusinessEventInput.model_validate(state["event"])
            name="crisis" if event.event_type.lower() in {"factoryfire","cyberattack","supplierbankruptcy","poweroutage","machinefailure","vendorbankruptcy"} else "procurement" if event.event_type.lower() in {"purchaserequest","vendordelay"} else "operations"
            import time
            started=time.perf_counter(); primary=await self.agents.get(name).execute(event); AGENT_EXECUTIONS.labels(name,"success").inc(); AGENT_LATENCY.labels(name).observe((time.perf_counter()-started)*1000)
            finance=await self.agents.get("finance").execute(RecommendationInput(event=event,recommendation=primary,available_budget=float(event.payload.get("budget_available",event.payload.get("budget",primary.estimated_cost)) or 0)))
            compliance=await self.agents.get("compliance").execute(RecommendationInput(event=event,recommendation=primary))
            coo=await self.agents.get("coo").execute(COOInput(**event.model_dump(),plan=None,policy=None))
            recommendations={name:primary.model_dump() if hasattr(primary,"model_dump") else primary,"finance":finance.model_dump(),"compliance":compliance.model_dump(),"coo":coo}
            return await persist(state,{"status":"awaiting_approval","recommendations":recommendations})
        async def approval(state):
            decision=interrupt({"workflow_id":state.get("workflow_id"),"action":"approve_recommendation","context":state.get("recommendations",{}),"expires_minutes":30}); return await persist(state,{"status":"approved" if decision.get("decision") in {"approved","modified"} else "rejected","approval":decision})
        async def execute(state): return await persist(state,{"status":"executing","execution":{"executed":True,"critical_action":"delegated_to_external_executor"}})
        async def audit(state):
            WORKFLOWS.labels(state.get("status","completed"),state.get("event",{}).get("event_type","unknown")).inc()
            return await persist(state,{"status":"completed","audit":[*state.get("audit",[]),{"action":"completed","snapshot":dict(state)}]})
        def route_policy(state)->Literal["reject","specialists"]: return "reject" if state.get("policy",{}).get("status")=="rejected" else "specialists"
        def route_specialists(state)->Literal["approval","reject"]:
            finance=state.get("recommendations",{}).get("finance",{}).get("status")
            compliance=state.get("recommendations",{}).get("compliance",{}).get("status")
            return "reject" if finance=="rejected" or compliance=="non_compliant" else "approval"
        def route_approval(state)->Literal["execute","reject"]: return "execute" if state.get("status")=="approved" else "reject"
        graph=StateGraph(WorkflowState); graph.add_node("classify",classify); graph.add_node("planner",plan); graph.add_node("policy",policy); graph.add_node("specialists",specialists); graph.add_node("approval",approval); graph.add_node("execute",execute); graph.add_node("audit",audit)
        graph.add_edge(START,"classify"); graph.add_edge("classify","planner"); graph.add_edge("planner","policy"); graph.add_conditional_edges("policy",route_policy,{"reject":"audit","specialists":"specialists"}); graph.add_conditional_edges("specialists",route_specialists,{"approval":"approval","reject":"audit"}); graph.add_conditional_edges("approval",route_approval,{"execute":"execute","reject":"audit"}); graph.add_edge("execute","audit"); graph.add_edge("audit",END)
        return graph.compile(checkpointer=checkpointer)
