from fastapi import APIRouter, Depends
from components.authentication.dependencies import CurrentUserDep

user_router = APIRouter()


@user_router.get('/info')
async def get_user_info(user: CurrentUserDep):
    return user
