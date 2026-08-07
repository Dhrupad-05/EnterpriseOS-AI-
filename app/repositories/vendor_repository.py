from dataclasses import dataclass
from typing import Protocol
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.operations import Vendor

@dataclass
class VendorMetrics:
    vendor_id: str
    name: str
    category: str
    on_time_deliveries: int
    total_orders: int
    avg_unit_cost: float
    quality_score: float
    avg_delivery_days: int
    late_deliveries: int
    available_capacity: int = 0
    price_premium: float = 0.0

class VendorRepository(Protocol):
    async def get_vendor_metrics(self, vendor_id: str, days: int = 90) -> VendorMetrics | None: ...
    async def list_by_category(self, category: str) -> list[VendorMetrics]: ...

class InMemoryVendorRepository:
    def __init__(self, vendors: list[VendorMetrics] | None = None): self.vendors = vendors or []
    async def get_vendor_metrics(self, vendor_id, days=90):
        return next((v for v in self.vendors if v.vendor_id == vendor_id), None)
    async def list_by_category(self, category):
        return [v for v in self.vendors if v.category == category]

class SQLAlchemyVendorRepository:
    def __init__(self, db: AsyncSession): self.db=db
    async def get_vendor_metrics(self,vendor_id,days=90):
        vendor=await self.db.get(Vendor,vendor_id)
        if not vendor: return None
        return VendorMetrics(str(vendor.id),vendor.name,vendor.category,round(vendor.on_time_delivery_rate*100),100,vendor.avg_unit_cost,vendor.performance_score,vendor.avg_delivery_days,vendor.late_deliveries_90d)
    async def list_by_category(self,category):
        rows=(await self.db.execute(select(Vendor).where(Vendor.category==category,Vendor.is_deleted.is_(False)))).scalars().all()
        return [VendorMetrics(str(v.id),v.name,v.category,round(v.on_time_delivery_rate*100),100,v.avg_unit_cost,v.performance_score,v.avg_delivery_days,v.late_deliveries_90d) for v in rows]
