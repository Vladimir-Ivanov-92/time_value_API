import pytest
from sqlalchemy import insert, select

from src.auth.models import Role
from tests.conftest import async_session_maker, client


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(name="admin", permission=None)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        role = result.fetchone()[
            0]  # Получаем первый элемент кортежа, который является объектом Role
        assert (role.id, role.name, role.permission) == (1, "admin", None)


def test_register():
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "username": "string",
        "role_id": 1
    })

    assert response.status_code == 201
