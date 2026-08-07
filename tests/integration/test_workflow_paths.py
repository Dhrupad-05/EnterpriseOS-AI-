from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from app.workflows.graph import WorkflowOrchestrator
async def test_policy_rejection_stops_before_execution():
    graph=WorkflowOrchestrator().build(MemorySaver()); config={"configurable":{"thread_id":"reject-path"}}
    state=await graph.ainvoke({"workflow_id":"reject-path","event":{"event_type":"PurchaseRequest","title":"blocked","description":"blocked","payload":{"amount":10,"vendor_status":"blacklisted"}}},config)
    assert state["status"]=="completed" and "execution" not in state and state["policy"]["status"]=="rejected"
async def test_crisis_approval_execution_path():
    graph=WorkflowOrchestrator().build(MemorySaver()); config={"configurable":{"thread_id":"crisis-path"}}
    paused=await graph.ainvoke({"workflow_id":"crisis-path","event":{"event_type":"VendorBankruptcy","title":"supplier failure","description":"critical supplier failed","severity":"critical","payload":{"daily_loss":2300000}}},config)
    assert paused["status"]=="awaiting_approval"
    done=await graph.ainvoke(Command(resume={"decision":"approved"}),config)
    assert done["status"]=="completed"
