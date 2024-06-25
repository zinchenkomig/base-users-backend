from typing import List

import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException, status

import json_schemes
from dependencies import AsyncSessionDep
from json_schemes import UserRead
from src.repo import user as user_repo
from src.dependencies import get_current_superuser

# Used here just for swagger integrated login

superuser_router = APIRouter(dependencies=[Depends(get_current_superuser)])


@superuser_router.get('/users/all')
async def get_users(async_session: AsyncSessionDep) -> List[UserRead]:
    return await user_repo.get_users(async_session)


@superuser_router.post('/users/delete')
async def delete_user(async_session: AsyncSessionDep, guid: str):
    try:
        await user_repo.delete_user(async_session, delete_user_id=guid)
        await async_session.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@superuser_router.post('/users/update')
async def update_user(async_session: AsyncSessionDep, guid: str, new_user_params: json_schemes.SuperuserUserUpdate):
    try:
        await user_repo.update_user(async_session, update_user_id=guid, new_user_params=new_user_params)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username conflict')
    await async_session.commit()

