import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ContactCreate, ContactUpdate
from src.database.models import Contact, User
from src.repository.contacts import ContactRepository


@pytest_asyncio.fixture
async def contact_repository(db_session: AsyncSession) -> ContactRepository:
    return ContactRepository(db_session)


class TestContactRepository:
    @pytest.mark.asyncio
    async def test_get_list(
        self, contact_repository: ContactRepository, user: User, contact: Contact
    ):
        result = await contact_repository.get_list(user.id)
        assert len(result) == 1
        assert result[0] == contact

    @pytest.mark.asyncio
    async def test_get(self, contact_repository: ContactRepository, contact: Contact):
        result = await contact_repository.get(contact.id)
        assert result == contact

    @pytest.mark.asyncio
    async def test_create(self, contact_repository: ContactRepository, user: User):
        payload = ContactCreate(
            first_name="New",
            last_name="Contact",
            email="new.contact@example.com",
            phone="0987654321",
        )
        result = await contact_repository.create(payload, user.id)
        assert result.first_name == payload.first_name
        assert result.user_id == user.id

    @pytest.mark.asyncio
    async def test_replace(
        self, contact_repository: ContactRepository, contact: Contact
    ):
        payload = ContactUpdate(
            first_name="Updated",
            last_name="Contact",
            email="updated.contact@example.com",
            phone="1112223333",
        )
        result = await contact_repository.replace(contact.id, payload)
        assert result.first_name == payload.first_name

    @pytest.mark.asyncio
    async def test_delete(
        self, contact_repository: ContactRepository, contact: Contact
    ):
        await contact_repository.delete(contact.id)
        result = await contact_repository.get_list(contact.user_id)
        assert len(result) == 0
