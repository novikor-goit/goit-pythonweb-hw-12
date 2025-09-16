from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import NoSuchEntityException
from src.api.schemas import ContactCreate, ContactUpdate
from src.database.models import Contact


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_list(
        self,
        user_id: int,
        skip: int | None = None,
        limit: int = 100,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> Sequence[Contact]:
        query = select(Contact).where(Contact.user_id == user_id).limit(limit)
        if first_name:
            query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            query = query.filter(Contact.email.ilike(f"%{email}%"))

        if skip is not None:
            query = query.offset(skip)

        contacts = await self.db.execute(query)
        return contacts.scalars().all()

    async def get(self, contact_id: int) -> Contact:
        try:
            result = await self.db.execute(select(Contact).filter_by(id=contact_id))
            return result.scalar_one()
        except NoResultFound:
            raise NoSuchEntityException("ID", contact_id)

    async def create(self, payload: ContactCreate, user_id: int) -> Contact:
        contact = Contact(**payload.model_dump(), user_id=user_id)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def replace(self, contact_id: int, payload: ContactUpdate) -> Contact:
        contact = await self.get(contact_id)
        for key, value in payload.model_dump().items():
            setattr(contact, key, value)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def delete(self, contact_id: int) -> None:
        stmt = delete(Contact).where(Contact.id == contact_id)
        await self.db.execute(stmt)
        await self.db.commit()
