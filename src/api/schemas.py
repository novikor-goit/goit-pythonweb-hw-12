from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, PastDate, ConfigDict, HttpUrl


class HTTPError(BaseModel):
    detail: str


class PersistedEntity(BaseModel):
    id: int


class ContactUpdate(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    birthday: PastDate | None = None


class ContactCreate(ContactUpdate):
    pass


class ContactModel(ContactUpdate, PersistedEntity):
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=255)
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    is_confirmed: bool
    avatar: HttpUrl | None
    model_config = ConfigDict(from_attributes=True)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str
