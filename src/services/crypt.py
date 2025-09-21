from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from src.conf.config import settings


class CryptService:
    def __init__(self):
        self.context = CryptContext(
            schemes=[settings.CRYPT_ALGORITHM], deprecated="auto"
        )

    def hash(self, password: str) -> str:
        return self.context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)


crypt = CryptService()


def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(data: dict) -> str:
    return create_jwt_token(
        data, timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES)
    )


def create_refresh_token(data: dict) -> str:
    return create_jwt_token(data, timedelta(days=settings.REFRESH_TOKEN_LIFETIME_DAYS))


def decode_jwt_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError as e:
        raise e
