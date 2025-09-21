import json
from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import NoSuchEntityException
from src.api.schemas import ContactCreate, ContactUpdate
from src.database.models import Contact
from src.services.cache import Cache


class ContactRepository:
    """Repository for managing contacts."""

    def __init__(self, session: AsyncSession):
        """Initializes the contact repository.

        Args:
            session (AsyncSession): The database session.
        """
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
        """Gets a list of contacts for a user.

        Args:
            user_id (int): The user ID.
            skip (int | None, optional): The number of contacts to skip. Defaults to None.
            limit (int, optional): The maximum number of contacts to return. Defaults to 100.
            first_name (str | None, optional): The first name to filter by. Defaults to None.
            last_name (str | None, optional): The last name to filter by. Defaults to None.
            email (str | None, optional): The email to filter by. Defaults to None.

        Returns:
            Sequence[Contact]: The list of contacts.
        """
        cache_key = (
            f"contacts:{user_id}:{skip}:{limit}:{first_name}:{last_name}:{email}"
        )
        cached_contacts = await Cache.client().get(cache_key)
        if cached_contacts:
            return [Contact(**contact) for contact in json.loads(cached_contacts)]

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
        result = contacts.scalars().all()
        await Cache.client().set(
            cache_key, json.dumps([contact.to_dict() for contact in result]), ex=3600
        )
        return result

    async def get(self, contact_id: int) -> Contact:
        """Gets a contact by ID.

        Args:
            contact_id (int): The contact ID.

        Returns:
            Contact: The contact.
        """
        try:
            result = await self.db.execute(select(Contact).filter_by(id=contact_id))
            return result.scalar_one()
        except NoResultFound:
            raise NoSuchEntityException("ID", contact_id)

    async def create(self, payload: ContactCreate, user_id: int) -> Contact:
        """Creates a new contact.

        Args:
            payload (ContactCreate): The contact data.
            user_id (int): The user ID.

        Returns:
            Contact: The created contact.
        """
        contact = Contact(**payload.model_dump(), user_id=user_id)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        await Cache.client().delete(f"contacts:{user_id}")
        return contact

    async def replace(self, contact_id: int, payload: ContactUpdate) -> Contact:
        """Replaces a contact.

        Args:
            contact_id (int): The contact ID.
            payload (ContactUpdate): The new contact data.

        Returns:
            Contact: The replaced contact.
        """
        contact = await self.get(contact_id)
        for key, value in payload.model_dump().items():
            setattr(contact, key, value)
        await self.db.commit()
        await self.db.refresh(contact)
        await Cache.client().delete(f"contacts:{contact.user_id}")
        return contact

    async def delete(self, contact_id: int) -> None:
        """Deletes a contact.

        Args:
            contact_id (int): The contact ID.
        """
        contact = await self.get(contact_id)
        stmt = delete(Contact).where(Contact.id == contact_id)
        await self.db.execute(stmt)
        await self.db.commit()
        await Cache.client().delete(f"contacts:{contact.user_id}")
