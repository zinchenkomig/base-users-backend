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


class UserRead(BaseORM):
    id: uuid.UUID
    username: str
    email: Optional[str]
    roles: list[str]


class UserReadTg(BaseORM):
    id: uuid.UUID
    username: str
    roles: list[str]


class UserUpdate(BaseModel):
    username: str
    email: str

