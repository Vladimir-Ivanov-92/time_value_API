from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.config import SECRET_JWT

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    """
    Создается стратегии аутентификации JSON Web Token (JWT) с заданными параметрами,
    такими как секретный ключ (SECRET_JWT) и продолжительность срока действия JWT
    в секундах (lifetime_seconds)
    """
    return JWTStrategy(secret=SECRET_JWT, lifetime_seconds=3600)


# Создается экземпляр AuthenticationBackend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# Создается экземпляр FastAPIUsers, который будет использоваться для
# управления пользователями.
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Переменная, которая будет использоваться для получения текущего
# аутентифицированного пользователя
current_user = fastapi_users.current_user()
