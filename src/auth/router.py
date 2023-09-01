from fastapi import APIRouter, Depends

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.models import User
from auth.schemas import UserCreate, UserRead

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



@auth_router.get("/protected-route")
def protected_route(user: User = Depends(current_user)) -> str:
    """
    Получение имени пользователя, если пользователь аутентифицированн
    с помощью JWT-токена
    """
    return f"Hello, {user.username}"


@auth_router.get("/unprotected-route")
def unprotected_route() -> str:
    """
    Получение сообщения, для всех пользователей, в т.ч. не аутентифицированных
    """
    return "Hello, anonym"
