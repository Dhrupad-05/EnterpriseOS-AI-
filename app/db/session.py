from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config.settings import get_settings
engine = create_async_engine(get_settings().database_url, future=True, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async def get_db():
    async with SessionLocal() as session:
        yield session
