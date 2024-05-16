from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from jose import jwt, JWTError, ExpiredSignatureError

from conf import settings
from conf.secrets import PASSWORD_ENCODING_SECRET
from dependencies import AsyncSessionDep
from . import crud
import db_models as db

apikey_cookie_getter = APIKeyCookie(name='login_token')


async def get_current_user(async_session: AsyncSessionDep, token=Depends(apikey_cookie_getter)) -> db.User:
    try:
        payload = jwt.decode(token, PASSWORD_ENCODING_SECRET, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_origin: str = payload.get("user_origin")
        if username is None:
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
    user = await crud.get_user(async_session, username=username, origin=user_origin)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not get user from crud",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

CurrentUserDep = Annotated[db.User, Depends(get_current_user)]

