import uuid
from typing import Any
from sqlalchemy import String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import TimestampedModel
class WorkflowInstance(TimestampedModel):
    __tablename__="workflow_instances"; event_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("business_events.id"),index=True); status: Mapped[str]=mapped_column(String(40),index=True); current_step: Mapped[str|None]=mapped_column(String(120)); state_snapshot: Mapped[dict[str,Any]]=mapped_column(JSON,default=dict); started_at: Mapped[Any|None]=mapped_column(DateTime(timezone=True)); completed_at: Mapped[Any|None]=mapped_column(DateTime(timezone=True))
class PolicyDecisionRecord(TimestampedModel):
    __tablename__="policy_decisions"; workflow_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("workflow_instances.id"),index=True); rule_violated: Mapped[str|None]=mapped_column(String(120)); decision: Mapped[str]=mapped_column(String(30)); reasoning: Mapped[str]=mapped_column(Text); matched_rules: Mapped[list[Any]]=mapped_column(JSON,default=list)
class ApprovalRequestRecord(TimestampedModel):
    __tablename__="approval_requests"; workflow_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("workflow_instances.id"),index=True); action: Mapped[str]=mapped_column(String(150)); context: Mapped[dict[str,Any]]=mapped_column(JSON,default=dict); requested_by: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id")); expires_at: Mapped[Any]=mapped_column(DateTime(timezone=True)); approved_by: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id")); decision: Mapped[str|None]=mapped_column(String(30),index=True); comment: Mapped[str|None]=mapped_column(Text)
