from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils import comms
from utils.db_connection import AsyncMainSession
from utils.db_connection_sync import SyncMainSession

from conf import settings


async def get_async_session():
    async_session = AsyncMainSession()
    try:
        yield async_session
    finally:
        await async_session.close()


# In case of sync testing
def get_sync_session():
    session = SyncMainSession()
    try:
        yield session
    finally:
        session.close()


def get_email_sender():
    return comms.Gmail(token=settings.GMAIL_API_TOKEN, from_="zinchenkomig.sup@gmail.com")


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
EmailSenderDep = Annotated[comms.EmailSender, Depends(get_email_sender)]
