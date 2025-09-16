from datetime import timedelta, datetime, UTC
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from src.conf.config import settings

crypt = CryptContext(schemes=[settings.CRYPT_ALGORITHM], deprecated="auto")


def create_access_token(
    sub: str,
    lifetime_minutes: int,
    data: Optional[dict] = None,
) -> str:
    if data is None:
        data = {}
    expire = datetime.now(UTC) + timedelta(minutes=lifetime_minutes)
    jwt_data = {"sub": sub, "exp": expire, **data}
    jwt_data.update({"exp": expire})
    token = jwt.encode(jwt_data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
