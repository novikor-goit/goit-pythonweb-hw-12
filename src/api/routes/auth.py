from fastapi import APIRouter, Depends, status, BackgroundTasks, Request
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import NoSuchEntityException
from src.api.schemas import (
    UserCreate,
    UserResponse,
    AccessTokenResponse,
    PasswordResetRequest,
    PasswordReset,
)
from src.conf.config import settings
from src.database.session_manager import get_db
from src.services.crypt import (
    crypt,
    create_access_token,
    decode_jwt_token,
    create_refresh_token,
)
from src.services.email import send_email_in_background
from src.services.users import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    data: UserCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    user_service = UserService(db)
    try:
        await user_service.get_by_username(data.username)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )
    except NoSuchEntityException:
        ...
    try:
        await user_service.get_by_email(str(data.email))
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    except NoSuchEntityException:
        ...
    data.password = crypt.hash(data.password)
    user = await user_service.create(data)
    token = create_access_token(data={"sub": str(data.email)})
    send_email_in_background(
        data.email,
        user.username,
        str(request.base_url),
        background_tasks,
        "Confirm your email",
        "email_confirmation.html",
        {
            "base_url": str(request.base_url).rstrip("/"),
            "username": user.username,
            "token": token,
        },
    )
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
    if not user.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please confirm your email first",
        )
    access_token = create_access_token(
        data={"sub": user.username, "token_type": "access"}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "token_type": "refresh"}
    )
    return AccessTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_LIFETIME_MINUTES * 60,
    )


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/refresh")),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_jwt_token(token)
        if payload["token_type"] != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
        username = payload["sub"]
        user = await UserService(db).get_by_username(username)
        access_token = create_access_token(
            data={"sub": user.username, "token_type": "access"}
        )
        refresh_token = create_refresh_token(
            data={"sub": user.username, "token_type": "refresh"}
        )
        return AccessTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_LIFETIME_MINUTES * 60,
        )
    except (JWTError, NoSuchEntityException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@router.get("/email/confirm/{token}", response_model=UserResponse)
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    email: str = decode_jwt_token(token)["sub"]
    service = UserService(db)
    try:
        return await service.confirm_email(email)
    except NoSuchEntityException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )


@router.post("/request-password-reset")
async def request_password_reset(
    data: PasswordResetRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    user_service = UserService(db)
    try:
        user = await user_service.get_by_email(str(data.email))
        if user:
            token = create_access_token(data={"sub": user.email})
            send_email_in_background(
                data.email,
                user.username,
                str(request.base_url),
                background_tasks,
                "Reset your password",
                "password_reset.html",
                {
                    "base_url": str(request.base_url).rstrip("/"),
                    "username": user.username,
                    "token": token,
                },
            )
        return {"message": "Password reset email sent"}
    except NoSuchEntityException:
        return {"message": "Password reset email sent"}


@router.post("/password-reset")
async def password_reset(data: PasswordReset, db: AsyncSession = Depends(get_db)):
    try:
        email = decode_jwt_token(data.token)["sub"]
        user_service = UserService(db)
        await user_service.update_password(email, data.new_password)
        return {"message": "Password reset successful"}
    except (JWTError, NoSuchEntityException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token or user does not exist",
        )
