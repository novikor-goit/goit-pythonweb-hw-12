from datetime import timedelta, datetime, UTC
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from src.conf.config import settings

crypt = CryptContext(schemes=[settings.CRYPT_ALGORITHM], deprecated="auto")


def create_jwt_token(
    sub: str,
    lifetime_minutes: Optional[int] = None,
    data: Optional[dict] = None,
) -> str:
    if data is None:
        data = {}
    jwt_data = {"sub": sub, "iat": datetime.now(UTC), **data}
    if lifetime_minutes is not None:
        jwt_data["exp"] = datetime.now(UTC) + timedelta(minutes=lifetime_minutes)

    token = jwt.encode(jwt_data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
