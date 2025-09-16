from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import NoSuchEntityException
from src.api.schemas import UserCreate, UserResponse, AccessTokenResponse
from src.conf.config import settings
from src.database.session_manager import get_db
from src.services.crypt import crypt, create_access_token
from src.services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = None
    try:
        user = await user_service.get_by_username(data.username)
    except NoSuchEntityException:
        ...
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )
    data.password = crypt.hash(data.password)
    user = await user_service.create(data)
    return user


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> AccessTokenResponse:
    user_service = UserService(db)
    user = await user_service.get_by_username(form_data.username)
    if not user or not crypt.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        sub=user.username, lifetime_minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES
    )
    return AccessTokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_LIFETIME_MINUTES * 60,
    )
