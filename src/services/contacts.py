from datetime import date, timedelta
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ContactCreate, ContactUpdate
from src.database.models import Contact, User
from src.repository.contacts import ContactRepository


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repo = ContactRepository(db)

    async def assert_contact_belongs_to_user(self, contact_id: int, user: User) -> None:
        contact = await self.repo.get(contact_id)
        if contact.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

    async def create_contact(self, payload: ContactCreate, user: User) -> Contact:
        return await self.repo.create(payload, user.id)

    async def get_contacts(
        self,
        user: User,
        skip: int | None = 0,
        limit: int = 100,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> Sequence[Contact]:
        return await self.repo.get_list(
            user.id, skip, limit, first_name, last_name, email
        )

    async def get_contact(self, contact_id: int):
        return await self.repo.get(contact_id)

    async def replace_contact(self, contact_id: int, payload: ContactUpdate):
        return await self.repo.replace(contact_id, payload)

    async def delete_contact(self, contact_id: int):
        return await self.repo.delete(contact_id)

    async def get_upcoming_birthdays(self, user: User) -> Sequence[Contact]:
        all_contacts = await self.repo.get_list(user.id)
        today = date.today()
        seven_days_from_now = today + timedelta(days=7)

        upcoming_birthdays_contacts = []

        for contact in all_contacts:
            if contact.birthday:
                birthday_this_year = contact.birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= seven_days_from_now:
                    upcoming_birthdays_contacts.append(contact)

        return upcoming_birthdays_contacts
