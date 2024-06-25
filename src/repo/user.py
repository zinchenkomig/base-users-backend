import fastapi
from fastapi import HTTPException
from sqlalchemy import select, delete, update


import db_models as models
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json_schemes


async def get_user(async_session, username=None, tg_id=None, user_id=None) -> Optional[models.User]:
    if username is None and tg_id is None and user_id is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="no identity specified")

    if tg_id is not None:
        query = select(models.User).filter_by(tg_id=tg_id).limit(1)
    if username is not None:
        query = select(models.User).filter_by(username=username).limit(1)
    if user_id is not None:
        query = select(models.User).filter_by(guid=user_id).limit(1)

    user_query_exec = await async_session.execute(query)
    user = user_query_exec.scalars().one_or_none()
    return user


async def check_is_user_exists(async_session, user_create):
    user_query_exec = await async_session.execute(select(models.User)
                                                  .filter((models.User.username == user_create.username)
                                                          | (models.User.email == user_create.email)).limit(1))
    user = user_query_exec.scalars().first()
    return user is not None


async def new_user(async_session, user):
    async_session.add(user)
    return user


async def verify_user(async_session, user_guid):
    user_query_exec = await async_session.execute(select(models.User).filter_by(guid=user_guid).limit(1))
    user = user_query_exec.scalars().one_or_none()
    if user is None:
        raise HTTPException(status_code=404)
    user.is_verified = True


async def get_users(async_session: AsyncSession) -> List[models.User]:
    users_resp = await async_session.execute(select(models.User).order_by(models.User.created_at.desc(),
                                                                          models.User.username))
    users = list(users_resp.scalars().all())
    return users


async def delete_user(async_session: AsyncSession, delete_user_id: str):
    await async_session.execute(delete(models.User).where(models.User.guid == delete_user_id))


async def update_user(async_session: AsyncSession, update_user_id: str, new_user_params):
    await async_session.execute(update(models.User).where(models.User.guid == update_user_id)
                                .values(**new_user_params.dict()))
