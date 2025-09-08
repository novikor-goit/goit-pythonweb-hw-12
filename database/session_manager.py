from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import AsyncIterator

from etc.config import config

engine = create_async_engine(config.DB_URL, echo=True)
async_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


async def db() -> AsyncIterator[AsyncSession]:
    async with async_maker() as session:
        try:
            yield session
        finally:
            await session.close()
