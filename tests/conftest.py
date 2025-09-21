import asyncio
from typing import Generator

import fakeredis.aioredis
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from src.database.models import Base, User, Contact
from src.database.session_manager import get_db
from src.services.cache import Cache
from src.services.crypt import crypt

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def override_get_db() -> Generator[AsyncSession, None, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True, scope="function")
def mock_redis(monkeypatch, mocker):
    monkeypatch.setattr(Cache, "_redis_client", fakeredis.FakeAsyncRedis())


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    user = User(
        username="testuser",
        email="test@example.com",
        password=crypt.hash("password"),
        is_confirmed=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def contact(db_session: AsyncSession, user: User) -> Contact:
    contact = Contact(
        first_name="Test",
        last_name="Contact",
        email="test.contact@example.com",
        phone="1234567890",
        user_id=user.id,
    )
    db_session.add(contact)
    await db_session.commit()
    await db_session.refresh(contact)
    return contact


@pytest.fixture()
def authenticated_client(client: TestClient, user: User) -> TestClient:
    response = client.post(
        "/api/auth/login",
        data={"username": user.username, "password": "password"},
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture()
def authenticated_client(client: TestClient, user: User) -> TestClient:
    response = client.post(
        "/api/auth/login",
        data={"username": user.username, "password": "password"},
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest_asyncio.fixture
async def admin(db_session: AsyncSession) -> User:
    user = User(
        username="admin",
        email="admin@example.com",
        password=crypt.hash("password"),
        is_confirmed=True,
        role="admin",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
