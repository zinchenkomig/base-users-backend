import fastapi
from fastapi import HTTPException
from sqlalchemy import select

from db_models import User
from typing import Optional


async def get_user(async_session, username=None, tg_id=None, user_id=None) -> Optional[User]:
    if username is None and tg_id is None and user_id is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="no identity specified")

    if tg_id is not None:
        query = select(User).filter_by(tg_id=tg_id).limit(1)
    if username is not None:
        query = select(User).filter_by(username=username).limit(1)
    if user_id is not None:
        query = select(User).filter_by(guid=user_id).limit(1)

    # query = query.filter_by(is_verified=True)
    user_query_exec = await async_session.execute(query)
    user = user_query_exec.scalars().one_or_none()
    return user


async def check_is_user_exists(async_session, user_create):
    user_query_exec = await async_session.execute(select(User)
                                                  .filter((User.username == user_create.username)
                                                          | (User.email == user_create.email)).limit(1))
    user = user_query_exec.scalars().first()
    return user is not None


async def new_user(async_session, user):
    async_session.add(user)
    return user


async def verify_user(async_session, user_guid):
    user_query_exec = await async_session.execute(select(User).filter_by(guid=user_guid).limit(1))
    user = user_query_exec.scalars().one_or_none()
    if user is None:
        raise HTTPException(status_code=404)
    user.is_verified = True
