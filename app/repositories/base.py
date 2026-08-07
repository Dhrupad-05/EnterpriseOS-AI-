from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import TimestampedModel
ModelT=TypeVar("ModelT",bound=TimestampedModel)
class Repository(Generic[ModelT]):
    def __init__(self,db:AsyncSession,model:type[ModelT]): self.db=db; self.model=model
    async def get(self,entity_id): return await self.db.get(self.model,entity_id)
    async def list(self,limit=100): return list((await self.db.execute(select(self.model).where(self.model.is_deleted.is_(False)).limit(limit))).scalars())
    async def add(self,entity): self.db.add(entity); await self.db.flush(); return entity
