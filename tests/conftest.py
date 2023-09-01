import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

from main import app
from src.auth.models import *
from src.config import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST,
                        DB_USER_TEST)
from src.database import Base, get_async_session
from src.value.models import *

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession,
                                         expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="session")
async def authenticated_client():
    client = TestClient(app)

    async with async_session_maker() as session:
        stmt = insert(Role).values(name="admin", permission=None)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        role = result.fetchone()[0]
        assert (role.id, role.name, role.permission) == (1, "admin", None), "role"

        response = client.post("/auth/register", json={
            "email": "user@example1.com",
            "password": "string1",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            "username": "string",
            "role_id": 1
        })

        assert response.status_code == 201, "register"

        login_data = {
            "username": "user@example1.com",
            "password": "string1",
        }

        response = client.post("/auth/jwt/login", data=login_data)
        assert response.status_code == 204, "login"

        cookie_header = response.headers.get('set-cookie')

        cookie_parts = cookie_header.split(';')

        for part in cookie_parts:
            if 'fastapiusersauth' in part:
                token = part.split('=')[1]
                break

    return client, token
