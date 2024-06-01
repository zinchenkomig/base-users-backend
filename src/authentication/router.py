from datetime import timedelta
from typing import Union, Dict, Any

from fastapi import APIRouter, Response, Depends, HTTPException, status, Request, Body
from fastapi.security import OAuth2PasswordRequestForm

from conf import settings
from conf.secrets import tg_secret_token
from db_models import User
from dependencies import AsyncSessionDep
from json_schemes import UserCreate, UserRead, UserReadTg
from . import crud
from .security import verify_password, get_password_hash, create_access_token, is_tg_hash_valid
from .roles import Role

auth_router = APIRouter()


async def authenticate_user(async_session, username: str, password: str) -> Union[User, bool]:
    user = await crud.get_user(async_session, username=username)
    if user is None:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@auth_router.post("/token", response_model=UserRead)
async def login_for_access_token(response: Response,
                                 async_session: AsyncSessionDep,
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(async_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": str(user.id),
            "login": user.username,
            "roles": user.roles},
        expires_delta=access_token_expires
    )
    response.set_cookie(key='login_token', value=access_token,
                        samesite=settings.SAME_SITE,
                        secure=settings.IS_SECURE_COOKIE,
                        httponly=True
                        )
    return user


@auth_router.post("/tg/login", response_model=UserReadTg)
async def auth_tg(response: Response, async_session: AsyncSessionDep, request: Dict[Any, Any]):
    if not is_tg_hash_valid(request, tg_secret_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed tg token verification",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = request.get('username')
    if request.get('id') is not None:
        tg_id = str(request.get('id'))
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='telegram id not specified')
    photo_url = request.get('photo_url')
    first_name = request.get('first_name')
    last_name = request.get('last_name')
    user = await crud.get_user(async_session, tg_id=tg_id)
    if user is None:
        user = User(username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=None,
                    password=None,
                    tg_id=tg_id,
                    is_active=True,
                    photo_url=photo_url,
                    roles=[Role.Reader.value]
                    )
        user = await crud.new_user(async_session, user)
        await async_session.commit()
        await async_session.refresh(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "id": str(user.id),
            "login": username,
            "roles": user.roles
              },
        expires_delta=access_token_expires
    )
    response.set_cookie(key='login_token', value=access_token,
                        samesite=settings.SAME_SITE,
                        secure=settings.IS_SECURE_COOKIE,
                        httponly=settings.IS_SECURE_COOKIE
                        )
    return user


@auth_router.post('/logout')
async def logout(response: Response):
    """
    Removes JWT token from http_only cookie
    :param response:
    :return:
    """
    response.set_cookie('login_token', value='', httponly=True,
                        samesite=settings.SAME_SITE, secure=settings.IS_SECURE_COOKIE)


@auth_router.post('/register')
async def register(user_create: UserCreate, response: Response,
                   async_session: AsyncSessionDep):
    """
    Registers a user
    :param response:
    :param user_create:
    :param async_session:
    :return:
    """
    if await crud.check_is_user_exists(async_session, user_create):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    else:
        hashed_pass = get_password_hash(user_create.password)
        user = User(username=user_create.username,
                    email=user_create.email,
                    password=hashed_pass,
                    is_active=True,
                    roles=[Role.Reader.value])
        await crud.new_user(async_session, user)
        await async_session.commit()
        response.status_code = status.HTTP_201_CREATED
