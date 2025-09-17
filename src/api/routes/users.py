from cloudinary.exceptions import BadRequest
from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import UserResponse
from src.database.models import User
from src.database.session_manager import get_db
from src.services.auth import get_current_user
from src.services.media import MediaStorage
from src.services.users import UserService

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/me",
    response_model=UserResponse,
    description="No more than 24 requests per minute",
)
@limiter.limit("24/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    return user


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        url = MediaStorage().upload_file(file, user.username)
    except BadRequest as e:
        raise HTTPException(status_code=400, detail=str(e))
    service = UserService(db)
    return await service.update_field(user, "avatar", url)
