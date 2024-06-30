import datetime

import fastapi
import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError

import json_schemes
from conf import settings
from conf.secrets import PASSWORD_ENCODING_SECRET
from dependencies import AsyncSessionDep, EmailSenderDep
from json_schemes import UserRead
from src.dependencies import CurrentUserDep
from src.repo import user as user_repo
from src.service.auth import create_access_token, get_password_hash

user_router = APIRouter()


@user_router.get('/info', response_model=UserRead)
async def get_user_info(user: CurrentUserDep):
    return user


@user_router.post('/update')
async def update_user(async_session: AsyncSessionDep,
                      new_user_params: json_schemes.UserUpdate,
                      current_user: CurrentUserDep):
    try:
        await user_repo.update_user(async_session, update_user_id=current_user.guid, new_user_params=new_user_params)
    except sqlalchemy.exc.IntegrityError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'db conflict: {err.detail}; {err}')
    await async_session.commit()


@user_router.post('/forgot_password')
async def forgot_password(async_session: AsyncSessionDep,
                          email_sender: EmailSenderDep,
                          email_data: json_schemes.Email):
    user = await user_repo.get_user(async_session, email=email_data.email)
    if user is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND)
    token = create_access_token(data={'user_guid': str(user.guid)}, expires_delta=datetime.timedelta(days=1))
    email_sender.send_with_retries(to=email_data.email, subject='Password Recovery',
                                   message_text=f"""
                                                                <html>
                                                                <body>
                                                                <h2>Hello, Dear Friend!</h2>
                                                                <p>To recover your password, please follow the link: 
                                                                {settings.FRONTEND_URL}/recover_password/{token}
                                                                </p>
                                                                </body>
                                                                </html>
                                                                """)


@user_router.post('/forgot_password/verify')
async def forgot_password(async_session: AsyncSessionDep, data: json_schemes.RecoverPassword):
    try:
        payload = jwt.decode(data.token, PASSWORD_ENCODING_SECRET, algorithms=[settings.ALGORITHM])
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

    user_guid = payload.get('user_guid')
    user = await user_repo.get_user(async_session, user_guid=user_guid)
    user.password = get_password_hash(data.new_password)
    await async_session.commit()
