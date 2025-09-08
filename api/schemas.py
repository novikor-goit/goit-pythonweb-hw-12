from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, PastDate, ConfigDict


class HTTPError(BaseModel):
    detail: str


class PersistedEntity(BaseModel):
    id: int


class ContactPayload(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    birthday: PastDate | None
    created_at: datetime
    updated_at: datetime


class ContactModel(ContactPayload, PersistedEntity):
    model_config = ConfigDict(from_attributes=True)
