import json
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.entities import AuditLog
from app.models.workflow_runtime import WorkflowInstance

class WorkflowPersistence:
    """Durable workflow-state writer: PostgreSQL is authoritative; Redis is an optional read cache."""
    def __init__(self, db: AsyncSession, redis_client=None):
        self.db=db
        self.redis=redis_client

    async def save(self, workflow_id: str, state: dict) -> None:
        now=datetime.now(timezone.utc)
        try:
            event_id=UUID(str(workflow_id))
        except ValueError:
            event_id=None
        instance=None
        if event_id:
            instance=(await self.db.execute(select(WorkflowInstance).where(WorkflowInstance.event_id==event_id))).scalar_one_or_none()
        if instance:
            instance.status=state.get("status",instance.status)
            instance.current_step=state.get("status",instance.current_step)
            instance.state_snapshot=state
            if state.get("status")=="completed": instance.completed_at=now
        self.db.add(AuditLog(action="workflow_state_snapshot",correlation_id=str(workflow_id),decision=state))
        await self.db.commit()
        if self.redis:
            await self.redis.set(f"workflow:snapshot:{workflow_id}",json.dumps({"saved_at":now.isoformat(),"state":state},default=str))

    async def load(self, workflow_id: str) -> dict | None:
        if self.redis:
            raw=await self.redis.get(f"workflow:snapshot:{workflow_id}")
            if raw: return json.loads(raw)["state"]
        try:
            event_id=UUID(str(workflow_id))
        except ValueError:
            return None
        instance=(await self.db.execute(select(WorkflowInstance).where(WorkflowInstance.event_id==event_id))).scalar_one_or_none()
        return instance.state_snapshot if instance else None

    async def replay(self, workflow_id: str) -> list[AuditLog]:
        return list((await self.db.execute(select(AuditLog).where(AuditLog.correlation_id==str(workflow_id)).order_by(AuditLog.created_at))).scalars())
