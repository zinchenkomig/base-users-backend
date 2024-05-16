from ..authentication.dependencies import get_current_user
from fastapi import Depends, HTTPException, status
import db_models as db


async def get_current_superuser(current_user: db.User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return current_user
