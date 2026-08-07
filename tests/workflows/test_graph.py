from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from app.workflows.graph import WorkflowOrchestrator
async def test_graph_pauses_and_replays_approval():
    graph=WorkflowOrchestrator().build(MemorySaver()); config={"configurable":{"thread_id":"test-graph"}}
    event={"event_type":"PurchaseRequest","title":"laptops","description":"buy","severity":"high","payload":{"amount":1000}}
    paused=await graph.ainvoke({"workflow_id":"test-graph","event":event},config)
    assert paused["status"]=="awaiting_approval" and paused["__interrupt__"]
    completed=await graph.ainvoke(Command(resume={"decision":"approved","comment":"approved by test"}),config)
    assert completed["status"]=="completed" and completed["execution"]["executed"]
