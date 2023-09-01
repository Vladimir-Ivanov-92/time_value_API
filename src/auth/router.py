from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.models import User
from auth.schemas import UserCreate, UserRead
from database import get_async_session

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@auth_router.get("/protected-route", response_model=UserRead)
async def protected_route(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)) -> UserRead:
    """
    Получение имени пользователя, если пользователь авторизирован
    """
    query = select(User)
    result = await session.execute(query)
    return result.scalar()


@auth_router.get("/unprotected-route")
def unprotected_route() -> str:
    """
    Получение сообщения, для всех пользователей, в т.ч. не авторизированных
    """
    return "Hello anonym!"
