from typing import Sequence
from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ContactPayload
from database.models import Contact
from repository.contacts import ContactRepository


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repo = ContactRepository(db)

    @staticmethod
    def _create_from_payload(payload: ContactPayload) -> Contact:
        return Contact(**payload.model_dump(exclude_unset=True))

    async def create_contact(self, payload: ContactPayload) -> Contact:
        contact = self._create_from_payload(payload)
        return await self.repo.save(contact)

    async def get_contacts(
        self,
        skip: int | None = 0,
        limit: int | None = 100,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
    ) -> Sequence[Contact]:
        return await self.repo.get_list(skip, limit, first_name, last_name, email)

    async def get_contact(self, contact_id: int):
        return await self.repo.get(contact_id)

    async def replace_contact(self, contact_id: int, payload: ContactPayload):
        updated_contact = self._create_from_payload(payload)
        updated_contact.id = contact_id
        return await self.repo.save(updated_contact)

    async def delete_contact(self, contact_id: int):
        return await self.repo.delete(contact_id)

    async def get_upcoming_birthdays(self) -> Sequence[Contact]:
        all_contacts = await self.repo.get_list()
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
