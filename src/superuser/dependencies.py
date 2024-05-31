from ..authentication.dependencies import get_current_user
from ..authentication.roles import Role
from fastapi import Depends, HTTPException, status
import db_models as db


async def get_current_superuser(current_user: db.User = Depends(get_current_user)):
    if Role.Admin.value not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return current_user
