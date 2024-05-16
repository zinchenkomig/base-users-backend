import db_models as db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import List

import json_schemes


async def get_users(async_session: AsyncSession) -> List[db.User]:
    users_resp = await async_session.execute(select(db.User).order_by(db.User.is_superuser.desc(), db.User.username))
    users = list(users_resp.scalars().all())
    return users


async def delete_user(async_session: AsyncSession, delete_user_id: str):
    await async_session.execute(delete(db.User).where(db.User.id == delete_user_id))


async def update_user(async_session: AsyncSession, update_user_id: str, new_user_params: json_schemes.UserUpdate):
    await async_session.execute(update(db.User).where(db.User.id == update_user_id).values(**new_user_params.dict()))
