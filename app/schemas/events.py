import uuid
from typing import Any
from pydantic import BaseModel, Field
from app.models.entities import EventStatus
class EventCreate(BaseModel):
    event_type: str = Field(min_length=1, max_length=100); source: str="api"; title: str; description: str; severity: str="medium"; payload: dict[str,Any]=Field(default_factory=dict)
class EventRead(EventCreate):
    id: uuid.UUID; status: EventStatus; classification: str|None=None
    model_config={"from_attributes":True}
class ApprovalDecision(BaseModel):
    status: str; comment: str|None=None; modified_action: dict[str,Any]|None=None
