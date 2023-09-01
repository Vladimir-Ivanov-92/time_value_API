import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, UUIDIDMixin, exceptions, models,
                           schemas)

from src.auth.models import User
from src.auth.utils import get_user_db
from src.config import SECRET_AUTH_MANAGER_KEY


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
     Менеджер пользователей для библиотеки fastapi-users.
     Этот класс обеспечивает управление пользователями, включая обработку
     различных событий, таких как регистрация, запрос на сброс пароля и
     запрос на верификацию.
    """
    reset_password_token_secret = SECRET_AUTH_MANAGER_KEY
    verification_token_secret = SECRET_AUTH_MANAGER_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Вызывается после успешной регистрации пользователя"""
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        """Вызывается после запроса на сброс пароля пользователя"""
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        """Вызывается после запроса на верификацию пользователя"""
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Cоздает и возвращает экземпляр UserManager с использованием зависимости user_db
    """
    yield UserManager(user_db)
