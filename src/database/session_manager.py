import contextlib
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from src.conf.config import settings


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager: "DatabaseSessionManager | None" = None


def get_session_manager() -> "DatabaseSessionManager":
    global sessionmanager
    if sessionmanager is None:
        sessionmanager = DatabaseSessionManager(settings.DB_URL)
    return sessionmanager


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    sm = get_session_manager()
    async with sm.session() as session:
        yield session
