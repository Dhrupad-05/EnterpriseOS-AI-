from uuid import UUID
from fastapi import APIRouter, Depends, Request, HTTPException, status
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import current_user
from app.db.session import get_db
from app.schemas.events import EventCreate, EventRead
from app.services.events import EventService
from app.workflows.graph import WorkflowOrchestrator
from app.models.entities import Approval, BusinessEvent
router=APIRouter(prefix="/events",tags=["Business Events"])
@router.post("",response_model=EventRead,status_code=status.HTTP_201_CREATED)
async def create_event(data:EventCreate,db:AsyncSession=Depends(get_db),user=Depends(current_user)):
    event,_=await EventService(db).ingest(data,user_id=UUID(user["sub"])); return event
@router.post("/{event_id}/orchestrate")
async def orchestrate_event(event_id:UUID,request:Request,db:AsyncSession=Depends(get_db),user=Depends(current_user)):
    event=await db.get(BusinessEvent,event_id)
    if not event: return {"error":"Event not found"}
    checkpointer=getattr(request.app.state,"workflow_checkpointer",None) or MemorySaver(); request.app.state.workflow_checkpointer=checkpointer
    graph=WorkflowOrchestrator().build(checkpointer); config={"configurable":{"thread_id":str(event_id)}}
    result=await graph.ainvoke({"workflow_id":str(event_id),"event":{"event_type":event.event_type,"source":event.source,"title":event.title,"description":event.description,"severity":event.severity,"payload":event.payload}},config)
    interrupt=result.get("__interrupt__")
    if interrupt:
        approval=Approval(event_id=event.id,requested_by=UUID(user["sub"]),expires_at=datetime.now(timezone.utc)+timedelta(minutes=30),urgency="critical" if event.severity=="critical" else "normal",proposed_action=result.get("recommendations",{})); db.add(approval); await db.commit()
    return {"event_id":str(event_id),"status":result.get("status"),"interrupt":bool(interrupt),"state":result}
@router.get("/{event_id}",response_model=EventRead)
async def get_event(event_id:UUID,db:AsyncSession=Depends(get_db),user=Depends(current_user)):
    event=await EventService(db).get(event_id)
    if not event: raise HTTPException(status_code=404,detail="Event not found")
    return event
@router.get("")
async def list_events(status_filter: str|None=None,limit:int=50,db:AsyncSession=Depends(get_db),user=Depends(current_user)):
    events=await EventService(db).list(status_filter,limit)
    return {"count":len(events),"events":[{"event_id":str(event.id),"type":event.event_type,"classification":event.classification,"status":event.status,"created_at":event.created_at} for event in events]}
