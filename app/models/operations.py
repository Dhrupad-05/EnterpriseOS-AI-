import uuid
from typing import Any
from sqlalchemy import String, Text, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import TimestampedModel
class Asset(TimestampedModel):
    __tablename__="assets"; name: Mapped[str]=mapped_column(String(200)); asset_type: Mapped[str]=mapped_column(String(80)); status: Mapped[str]=mapped_column(String(40),default="active"); metadata_: Mapped[dict[str,Any]]=mapped_column("metadata",JSON,default=dict)
class Inventory(TimestampedModel):
    __tablename__="inventory"; sku: Mapped[str]=mapped_column(String(100),unique=True,index=True); quantity: Mapped[int]=mapped_column(Integer,default=0); reorder_point: Mapped[int]=mapped_column(Integer,default=0); location: Mapped[str]=mapped_column(String(120))
class Vendor(TimestampedModel):
    __tablename__="vendors"; name: Mapped[str]=mapped_column(String(200),index=True); category: Mapped[str]=mapped_column(String(100),default="general",index=True); risk_score: Mapped[float]=mapped_column(Float,default=0); performance_score: Mapped[float]=mapped_column(Float,default=0); on_time_delivery_rate: Mapped[float]=mapped_column(Float,default=0); avg_unit_cost: Mapped[float]=mapped_column(Float,default=0); avg_delivery_days: Mapped[int]=mapped_column(Integer,default=0); late_deliveries_90d: Mapped[int]=mapped_column(Integer,default=0); metadata_: Mapped[dict[str,Any]]=mapped_column("metadata",JSON,default=dict)
class PurchaseOrder(TimestampedModel):
    __tablename__="purchase_orders"; vendor_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("vendors.id")); amount: Mapped[float]=mapped_column(Float); currency: Mapped[str]=mapped_column(String(3),default="USD"); status: Mapped[str]=mapped_column(String(40),default="draft"); line_items: Mapped[list[Any]]=mapped_column(JSON,default=list)
class Incident(TimestampedModel):
    __tablename__="incidents"; event_id: Mapped[uuid.UUID|None]=mapped_column(ForeignKey("business_events.id")); category: Mapped[str]=mapped_column(String(80)); impact: Mapped[str]=mapped_column(Text); severity: Mapped[str]=mapped_column(String(30)); response_plan: Mapped[dict[str,Any]]=mapped_column(JSON,default=dict)
class Equipment(TimestampedModel):
    __tablename__="equipment"; asset_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("assets.id")); serial_number: Mapped[str]=mapped_column(String(120),unique=True); health_score: Mapped[float]=mapped_column(Float,default=1)
class Policy(TimestampedModel):
    __tablename__="policies"; name: Mapped[str]=mapped_column(String(150),index=True); event_types: Mapped[list[Any]]=mapped_column(JSON,default=list); rules: Mapped[dict[str,Any]]=mapped_column(JSON,default=dict); priority: Mapped[int]=mapped_column(Integer,default=0); is_active: Mapped[bool]=mapped_column(default=True)
class AgentExecution(TimestampedModel):
    __tablename__="agent_executions"; event_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("business_events.id")); agent_name: Mapped[str]=mapped_column(String(100),index=True); status: Mapped[str]=mapped_column(String(40)); provider: Mapped[str|None]=mapped_column(String(60)); latency_ms: Mapped[int|None]=mapped_column(Integer); tokens: Mapped[int|None]=mapped_column(Integer)
class AgentDecision(TimestampedModel):
    __tablename__="agent_decisions"; execution_id: Mapped[uuid.UUID]=mapped_column(ForeignKey("agent_executions.id")); decision: Mapped[dict[str,Any]]=mapped_column(JSON); confidence: Mapped[float]=mapped_column(Float); rationale: Mapped[str]=mapped_column(Text)
class Metric(TimestampedModel):
    __tablename__="metrics"; name: Mapped[str]=mapped_column(String(120),index=True); value: Mapped[float]=mapped_column(Float); dimensions: Mapped[dict[str,Any]]=mapped_column(JSON,default=dict)
class Analytic(TimestampedModel):
    __tablename__="analytics"; name: Mapped[str]=mapped_column(String(120),index=True); result: Mapped[dict[str,Any]]=mapped_column(JSON,default=dict); period: Mapped[str]=mapped_column(String(50))
