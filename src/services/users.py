from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import UserCreate
from src.database.models import User
from src.repository.users import UserRepository


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create(self, payload: UserCreate) -> User:
        return await self.repository.create(payload)

    async def get_by_id(self, user_id: int) -> User:
        return await self.repository.get_by_id(user_id)

    async def get_by_username(self, username: str) -> User:
        return await self.repository.get_by_username(username)

    async def get_by_email(self, email: str) -> User:
        return await self.repository.get_by_email(email)

    async def confirm_email(self, email: str) -> User:
        user = await self.get_by_email(email)
        if not user.is_confirmed:
            user.is_confirmed = True
            await self.repository.save(user)
        return user
