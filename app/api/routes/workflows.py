from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import current_user
from app.db.session import get_db
from app.models.entities import AuditLog
from app.models.workflow_runtime import WorkflowInstance
router=APIRouter(prefix="/workflows",tags=["Workflows"])
@router.get("/{workflow_id}/replay")
async def replay_workflow(workflow_id:UUID,db:AsyncSession=Depends(get_db),user=Depends(current_user)):
    instance=await db.get(WorkflowInstance,workflow_id)
    logs=(await db.execute(select(AuditLog).where(AuditLog.correlation_id==str(workflow_id)).order_by(AuditLog.created_at))).scalars().all()
    if not instance and not logs: raise HTTPException(status_code=404,detail="Workflow not found")
    return {"workflow_id":str(workflow_id),"status":instance.status if instance else None,"timeline":[{"timestamp":log.created_at,"action":log.action,"decision":log.decision,"confidence":log.confidence,"latency_ms":log.latency_ms,"tokens":log.tokens} for log in logs],"total_snapshots":len(logs)}
