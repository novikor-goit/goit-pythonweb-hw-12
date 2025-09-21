from fastapi import Depends, HTTPException, status

from src.database.models import User
from src.database.role import Role
from src.services.auth import get_current_user


def is_admin(user: User = Depends(get_current_user)):
    if user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators have access to this resource",
        )
