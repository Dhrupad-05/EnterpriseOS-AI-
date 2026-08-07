import asyncio
from langgraph.checkpoint.memory import MemorySaver
from app.workflows.graph import WorkflowOrchestrator
async def test_100_concurrent_workflows():
    orchestrator=WorkflowOrchestrator(); graphs=[orchestrator.build(MemorySaver()) for _ in range(100)]
    async def run(index):
        config={"configurable":{"thread_id":f"load-{index}"}}
        return await graphs[index].ainvoke({"workflow_id":f"load-{index}","event":{"event_type":"PurchaseRequest","title":"load","description":"load","payload":{"amount":100}}},config)
    results=await asyncio.gather(*(run(i) for i in range(100)))
    assert len(results)==100 and all(result["status"]=="awaiting_approval" for result in results)
