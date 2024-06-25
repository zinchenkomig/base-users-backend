import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, status

import json_schemes
from dependencies import AsyncSessionDep
from json_schemes import UserRead
from src.dependencies import CurrentUserDep
from src.repo import user as user_repo

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
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username conflict')
    await async_session.commit()
