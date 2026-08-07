import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.entities import BusinessEvent
from app.schemas.events import EventCreate
from app.workflows.engine import WorkflowEngine
class EventService:
    def __init__(self,db:AsyncSession,engine:WorkflowEngine|None=None): self.db=db; self.engine=engine or WorkflowEngine()
    async def create(self,data:EventCreate,user_id:uuid.UUID):
        event=BusinessEvent(**data.model_dump(),created_by=user_id); self.db.add(event); await self.db.commit(); await self.db.refresh(event); return event
    async def transition(self,event,target): event.status=self.engine.transition(event.status,target); await self.db.commit(); await self.db.refresh(event); return event
