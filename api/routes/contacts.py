from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ContactModel, ContactPayload
from database.session_manager import db
from services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactModel])
async def get_contacts_list(
    skip: int = 0,
    limit: int = 100,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    db: AsyncSession = Depends(db),
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(
        skip, limit, first_name, last_name, email
    )
    return contacts


@router.get("/birthdays/", response_model=List[ContactModel])
async def get_upcoming_birthdays(db: AsyncSession = Depends(db)):
    contact_service = ContactService(db)
    contacts = await contact_service.get_upcoming_birthdays()
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
async def get_single_contact(contact_id: int, db: AsyncSession = Depends(db)):
    contact_service = ContactService(db)
    return await contact_service.get_contact(contact_id)


@router.post("/", response_model=ContactModel, status_code=status.HTTP_201_CREATED)
async def create_contact(
    payload: ContactPayload,
    db: AsyncSession = Depends(db),
):
    contact_service = ContactService(db)
    contact = await contact_service.create_contact(payload)
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
    body: ContactPayload, contact_id: int, db: AsyncSession = Depends(db)
):
    contact_service = ContactService(db)
    contact = await contact_service.replace_contact(contact_id, body)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(db)):
    contact_service = ContactService(db)
    await contact_service.delete_contact(contact_id)
