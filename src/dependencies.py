from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from jose import jwt, JWTError, ExpiredSignatureError

import db_models as db
from conf import settings
from conf.secrets import PASSWORD_ENCODING_SECRET
from dependencies import AsyncSessionDep
from src.repo import user as user_repo
from src.roles import Role


apikey_cookie_getter = APIKeyCookie(name='login_token', auto_error=False)


async def get_current_user(async_session: AsyncSessionDep, token=Depends(apikey_cookie_getter),
                           fake_user: Annotated[str | None, fastapi.Header()] = None,
                           fake_roles: Annotated[str | None, fastapi.Header()] = None
                           ) -> db.User:
    if not settings.IS_PROD and fake_user is not None and fake_roles is not None:
        user = await user_repo.get_user(async_session, username=fake_user)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {fake_user} not found")
        user.roles = fake_roles.split(',')
        return user
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token in cookie or cookie expired")
    try:
        payload = jwt.decode(token, PASSWORD_ENCODING_SECRET, algorithms=[settings.ALGORITHM])
        user_id = payload.get("guid")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not get user from jwt",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token signature expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"jwt error: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await user_repo.get_user(async_session, user_guid=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not get user from user_repo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

CurrentUserDep = Annotated[db.User, Depends(get_current_user)]


async def get_current_superuser(current_user: db.User = Depends(get_current_user)):
    if Role.Admin.value not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return current_user
