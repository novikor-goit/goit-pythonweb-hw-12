from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import NoSuchEntityException
from src.database.models import User
from src.database.session_manager import get_db
from src.services.crypt import decode_jwt_token
from src.services.users import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """Decodes the access token, retrieves the user from the database, and returns the user object.

    Args:
        token (str, optional): The access token. Defaults to Depends(oauth2_scheme).
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the token is invalid or the user is not found.

    Returns:
        User: The current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_jwt_token(token)
        if payload.get("token_type") != "access":
            raise credentials_exception
        username = payload["sub"]
        if username is None:
            raise credentials_exception
        return await UserService(db).get_by_username(username)
    except (JWTError, NoSuchEntityException):
        raise credentials_exception
