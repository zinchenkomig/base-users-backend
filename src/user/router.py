from fastapi import APIRouter, Depends
from src.authentication.dependencies import CurrentUserDep
from json_schemes import UserRead

user_router = APIRouter()


@user_router.get('/info', response_model=UserRead)
async def get_user_info(user: CurrentUserDep):
    return user
