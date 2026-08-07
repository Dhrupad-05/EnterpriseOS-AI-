from typing import Any, TypedDict
from app.agents.contract import Agent
class AgentState(TypedDict, total=False):
    input: dict[str, Any]
    output: Any
    error: str
class AgentSubgraphFactory:
    """Wraps every typed agent in an isolated LangGraph subgraph with one controlled boundary."""
    @staticmethod
    def build(agent: Agent, checkpointer=None):
        from langgraph.graph import END, START, StateGraph
        async def invoke(state):
            try:
                result=await agent.execute(state["input"])
                return {"output": result.model_dump() if hasattr(result,"model_dump") else result}
            except Exception as exc: return {"error": f"{agent.name}: {exc}"}
        graph=StateGraph(AgentState); graph.add_node(agent.name,invoke); graph.add_edge(START,agent.name); graph.add_edge(agent.name,END)
        return graph.compile(checkpointer=checkpointer)
