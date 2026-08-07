from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from langgraph.types import Command
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import current_user
from app.db.session import get_db
from app.models.entities import Approval, ApprovalStatus
from app.workflows.graph import WorkflowOrchestrator
from app.schemas.events import ApprovalDecision
router=APIRouter(prefix="/approvals",tags=["Approvals"])
@router.get("")
async def list_pending(db:AsyncSession=Depends(get_db),user=Depends(current_user)):
    rows=(await db.execute(select(Approval).where(Approval.status==ApprovalStatus.PENDING,Approval.is_deleted.is_(False)))).scalars().all()
    return [{"id":str(row.id),"event_id":str(row.event_id),"action":row.proposed_action,"status":row.status,"expires_at":row.expires_at,"expired":bool(row.expires_at and row.expires_at<=datetime.now(timezone.utc))} for row in rows]
@router.post("/{approval_id}/decision")
async def decide(approval_id:UUID,data:ApprovalDecision,request:Request,db:AsyncSession=Depends(get_db),user=Depends(current_user)):
    approval=await db.get(Approval,approval_id)
    if not approval or approval.status!=ApprovalStatus.PENDING: raise HTTPException(status_code=404,detail="Pending approval not found")
    try: approval.status=ApprovalStatus(data.status)
    except ValueError as exc: raise HTTPException(status_code=422,detail="Decision must be approved, rejected, or modified") from exc
    approval.comment=data.comment; approval.decided_by=UUID(user["sub"]); await db.commit()
    checkpointer=getattr(request.app.state,"workflow_checkpointer",None)
    resumed=False
    if checkpointer:
        graph=WorkflowOrchestrator().build(checkpointer); await graph.ainvoke(Command(resume={"decision":approval.status.value,"comment":data.comment}),{"configurable":{"thread_id":str(approval.event_id)}}); resumed=True
    return {"id":str(approval.id),"status":approval.status,"resumed":resumed}
