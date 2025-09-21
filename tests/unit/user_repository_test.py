import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import UserCreate
from src.database.models import User
from src.repository.users import UserRepository


@pytest_asyncio.fixture
async def user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create(self, user_repository: UserRepository):
        payload = UserCreate(
            username="newuser",
            email="new.user@example.com",
            password="newpassword",
        )
        result = await user_repository.create(payload)
        assert result.username == payload.username

    @pytest.mark.asyncio
    async def test_get_by_id(self, user_repository: UserRepository, user: User):
        result = await user_repository.get_by_id(user.id)
        assert result == user

    @pytest.mark.asyncio
    async def test_get_by_username(self, user_repository: UserRepository, user: User):
        result = await user_repository.get_by_username(user.username)
        assert result == user

    @pytest.mark.asyncio
    async def test_get_by_email(self, user_repository: UserRepository, user: User):
        result = await user_repository.get_by_email(user.email)
        assert result == user

    @pytest.mark.asyncio
    async def test_save(self, user_repository: UserRepository, user: User):
        user.username = "updateduser"
        result = await user_repository.save(user)
        assert result.username == "updateduser"
