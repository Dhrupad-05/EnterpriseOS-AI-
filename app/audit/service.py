from sqlalchemy.ext.asyncio import AsyncSession
from app.models.entities import AuditLog
class AuditService:
    def __init__(self,db:AsyncSession): self.db=db
    async def record(self,**values):
        row=AuditLog(**values); self.db.add(row); await self.db.flush(); return row
