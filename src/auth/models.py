from datetime import datetime
import uuid

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import Boolean, Column, String, DateTime, Integer, JSON, \
    ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

UUID_ID = uuid.UUID


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    permission = Column(JSON)


class User(SQLAlchemyBaseUserTableUUID, Base):
    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String(length=120), nullable=False)

    registered_at: Mapped[DateTime] = mapped_column(DateTime,
                                                    default=datetime.utcnow)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(Role.id))
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
