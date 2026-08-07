import uuid
from typing import ClassVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.entities import BusinessEvent, EventStatus
from app.models.workflow_runtime import WorkflowInstance
from app.schemas.events import EventCreate
from app.workflows.engine import WorkflowEngine
class EventService:
    CLASSIFICATION: ClassVar[dict[str,str]]={"PURCHASEREQUEST":"PROCUREMENT","VENDORDELAY":"PROCUREMENT","VENDORBANKRUPTCY":"CRISIS","SUPPLIERISSUE":"PROCUREMENT","FACTORYFIRE":"CRISIS","CYBERATTACK":"CRISIS","POWERFAILURE":"CRISIS","MACHINEFAILURE":"CRISIS","INVENTORYCOLLAPSE":"CRISIS","EQUIPMENTFAILURE":"OPERATIONS","EMPLOYEEINJURY":"OPERATIONS","CUSTOMERESCALATION":"OPERATIONS","COMPLIANCEISSUE":"COMPLIANCE","BUDGETOVERAGE":"FINANCE","INVOICEDISPUTE":"FINANCE","REFUNDREQUEST":"FINANCE"}
    def __init__(self,db:AsyncSession,engine:WorkflowEngine|None=None): self.db=db; self.engine=engine or WorkflowEngine()
    async def create(self,data:EventCreate,user_id:uuid.UUID):
        event=BusinessEvent(**data.model_dump(),created_by=user_id); self.db.add(event); await self.db.commit(); await self.db.refresh(event); return event
    async def ingest(self,data:EventCreate,user_id:uuid.UUID):
        event=await self.create(data,user_id); normalized="".join(ch for ch in event.event_type.upper() if ch.isalnum()); event.classification=self.CLASSIFICATION.get(normalized,"OPERATIONS"); event.status=EventStatus.CLASSIFIED
        instance=WorkflowInstance(event_id=event.id,status=event.status.value,current_step="classified",state_snapshot={"event_id":str(event.id),"classification":event.classification}); self.db.add(instance); await self.db.commit(); await self.db.refresh(event); return event,instance
    async def transition(self,event,target): event.status=self.engine.transition(event.status,target); await self.db.commit(); await self.db.refresh(event); return event
    async def get(self,event_id): return await self.db.get(BusinessEvent,event_id)
    async def list(self,status=None,limit=50):
        query=select(BusinessEvent).where(BusinessEvent.is_deleted.is_(False)).order_by(BusinessEvent.created_at.desc()).limit(limit)
        if status: query=query.where(BusinessEvent.status==status)
        return list((await self.db.execute(query)).scalars().all())
