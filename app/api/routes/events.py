from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import current_user
from app.db.session import get_db
from app.schemas.events import EventCreate, EventRead
from app.services.events import EventService
router=APIRouter(prefix="/events",tags=["Business Events"])
@router.post("",response_model=EventRead,status_code=status.HTTP_201_CREATED)
async def create_event(data:EventCreate,db:AsyncSession=Depends(get_db),user=Depends(current_user)):
    return await EventService(db).create(data,user_id=UUID(user["sub"]))
