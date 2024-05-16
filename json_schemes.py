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
    is_superuser: bool


class UserReadTg(BaseORM):
    id: uuid.UUID
    username: str
    is_superuser: bool


class UserUpdate(BaseModel):
    username: str
    email: str

