import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr

from src.auth.models import UUID_ID


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: UUID_ID
    username: str
    email: EmailStr
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    id: UUID_ID
    username: str
    email: EmailStr
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
