from conf import secrets
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils import comms
from utils import s3
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
    if settings.IS_PROD:
        return comms.Gmail(token=settings.GMAIL_API_TOKEN, from_="zinchenkomig.sup@gmail.com")
    return comms.MockSender()


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
EmailSenderDep = Annotated[comms.EmailSender, Depends(get_email_sender)]
S3PublicDep = Annotated[s3.S3Storage, Depends(lambda: s3.S3Storage(endpoint=settings.S3_ENDPOINT,
                                                                   access_key=secrets.s3_access_key,
                                                                   secret_key=secrets.s3_secret_key,
                                                                   bucket_name=settings.BUCKET,
                                                                   ))]
