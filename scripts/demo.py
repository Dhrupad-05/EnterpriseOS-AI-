"""Run the two judge-facing EnterpriseOS workflows without external credentials."""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from app.workflows.graph import WorkflowOrchestrator

async def run_case(thread_id: str, event: dict) -> None:
    graph=WorkflowOrchestrator().build(MemorySaver())
    config={"configurable":{"thread_id":thread_id}}
    paused=await graph.ainvoke({"workflow_id":thread_id,"event":event},config)
    print(f"{event['event_type']}: {paused['status']}")
    for agent,output in paused.get("recommendations",{}).items():
        print(f"  {agent}: {output}")
    completed=await graph.ainvoke(Command(resume={"decision":"approved","comment":"Demo approval"}),config)
    print(f"  completed: {completed['status']} | execution: {completed.get('execution')}")

async def main() -> None:
    await run_case("demo-purchase",{"event_type":"PurchaseRequest","title":"Electronics replenishment","description":"Request 100 units.","severity":"high","payload":{"category":"electronics","quantity":100,"budget":50000,"amount":45000}})
    await run_case("demo-crisis",{"event_type":"VendorBankruptcy","title":"Primary supplier bankruptcy","description":"Supplier filed for protection.","severity":"critical","payload":{"type":"VENDOR_BANKRUPTCY","daily_loss":2300000,"employees_affected":500,"recovery_budget":100000}})

if __name__=="__main__": asyncio.run(main())
