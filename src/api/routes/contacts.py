from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ContactModel, ContactCreate, ContactUpdate
from src.database.models import User
from src.database.session_manager import get_db
from src.services.auth import get_current_user
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactModel])
async def get_contacts_list(
    user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = ContactService(db)
    contacts = await service.get_contacts(
        user, skip, limit, first_name, last_name, email
    )
    return contacts


@router.get("/birthdays/", response_model=List[ContactModel])
async def get_upcoming_birthdays(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    service = ContactService(db)
    contacts = await service.get_upcoming_birthdays(user)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"message": "No such entity with ID {id}"}
                }
            }
        }
    },
)
async def get_single_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    await service.assert_contact_belongs_to_user(contact_id, user)
    return await service.get_contact(contact_id)


@router.post("/", response_model=ContactModel, status_code=status.HTTP_201_CREATED)
async def create_contact(
    payload: ContactCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    contact = await service.create_contact(payload, user)
    return contact


@router.put(
    "/{contact_id}",
    response_model=ContactModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"message": "No such entity with ID {id}"}
                }
            }
        }
    },
)
async def update_contact(
    body: ContactUpdate,
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    await service.assert_contact_belongs_to_user(contact_id, user)
    contact = await service.replace_contact(contact_id, body)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    await service.assert_contact_belongs_to_user(contact_id, user)
    await service.delete_contact(contact_id)
