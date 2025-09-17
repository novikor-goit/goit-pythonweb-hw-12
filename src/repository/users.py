from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import NoSuchEntityException
from src.api.schemas import UserCreate
from src.database.models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: UserCreate) -> User:
        user = User(**payload.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise NoSuchEntityException("ID", user_id)
        return user

    async def get_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise NoSuchEntityException("username", username)
        return user

    async def get_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise NoSuchEntityException("email", email)
        return user

    async def save(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user
