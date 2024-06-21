from typing import Optional

from pydantic import BaseModel
import uuid


class BaseORM(BaseModel):

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserGUID(BaseModel):
    user_guid: uuid.UUID


class UserRead(BaseORM):
    guid: uuid.UUID
    username: str
    email: Optional[str]
    roles: list[str]
    photo_url: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class UserReadTg(BaseORM):
    guid: uuid.UUID
    username: str
    roles: list[str]


class UserUpdate(BaseModel):
    username: str
    email: str
    roles: list[str]

