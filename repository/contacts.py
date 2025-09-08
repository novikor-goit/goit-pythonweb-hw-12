from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from api.exceptions import NoSuchEntityException
from database.models import Contact


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_list(
        self,
        skip: int | None = None,
        limit: int = 100,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> Sequence[Contact]:
        query = select(Contact).limit(limit)
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
        async with self.db.begin():
            try:
                result = await self.db.execute(select(Contact).filter_by(id=contact_id))
                return result.scalar_one()
            except NoResultFound:
                raise NoSuchEntityException(contact_id)

    async def save(self, contact: Contact) -> Contact:
        async with self.db.begin():
            contact = await self.db.merge(contact)
        return contact

    async def delete(self, contact_id: int) -> None:
        async with self.db.begin():
            result = await self.db.execute(select(Contact).filter_by(id=contact_id))
            contact = result.scalar_one_or_none()
            if contact:
                await self.db.delete(contact)
