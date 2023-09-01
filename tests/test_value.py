import http
from datetime import datetime

from httpx import AsyncClient
from sqlalchemy import insert, text

from src.value.models import Value
from tests.conftest import async_session_maker


async def test_get_minute_aggregated_data(async_client: AsyncClient,
                                          authenticated_client):
    create_function_sql = """
            CREATE OR REPLACE FUNCTION insert_random_value()
            RETURNS VOID AS $$
            BEGIN
                INSERT INTO value (time, value)
                VALUES (NOW(), CAST((RANDOM() * 10) AS NUMERIC(10, 2)));
            END;
            $$ LANGUAGE plpgsql;
        """
    create_triger_function_sql = """
                CREATE OR REPLACE FUNCTION trigger_insert_value_greater_than_9()
                RETURNS TRIGGER AS $$
                BEGIN
                    IF NEW.value > 9 THEN
                        INSERT INTO trigger_time (time) VALUES (NOW());
                    END IF;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """

    create_triger_sql = """
                CREATE TRIGGER insert_value_greater_than_9_trigger
                BEFORE INSERT ON value
                FOR EACH ROW
                EXECUTE FUNCTION trigger_insert_value_greater_than_9();
            """
    async with async_session_maker() as session:
        await session.execute(text(create_function_sql))
        await session.execute(text(create_triger_function_sql))
        await session.execute(text(create_triger_sql))
        await session.commit()

    async with async_session_maker() as session:
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:32:30.335", "%Y-%m-%d %H:%M:%S.%f"),
            value=4.67)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:32:35.371", "%Y-%m-%d %H:%M:%S.%f"),
            value=7.29)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:32:40.411", "%Y-%m-%d %H:%M:%S.%f"),
            value=3.64)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:32:45.437", "%Y-%m-%d %H:%M:%S.%f"),
            value=9.43)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:32:50.478", "%Y-%m-%d %H:%M:%S.%f"),
            value=9.24)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:32:55.512", "%Y-%m-%d %H:%M:%S.%f"),
            value=4.77)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:33:00.535", "%Y-%m-%d %H:%M:%S.%f"),
            value=6.16)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:33:05.592", "%Y-%m-%d %H:%M:%S.%f"),
            value=8.24)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:33:10.630", "%Y-%m-%d %H:%M:%S.%f"),
            value=9.1)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:33:15.659", "%Y-%m-%d %H:%M:%S.%f"),
            value=9.49)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:33:20.687", "%Y-%m-%d %H:%M:%S.%f"),
            value=7.72)
        await session.execute(stmt)
        stmt = insert(Value).values(
            time=datetime.strptime("2023-09-01 18:33:25.718", "%Y-%m-%d %H:%M:%S.%f"),
            value=1.59)
        await session.execute(stmt)
        await session.execute(stmt)
        await session.commit()

        client, token = authenticated_client

        cookie = http.cookies.SimpleCookie()
        cookie['fastapiusersauth'] = token

        cookie_str = cookie.output(header='', sep='; ')

        print(f"{cookie_str=}")

        response = client.get("/value/agr", headers={'Cookie': cookie_str})

        assert response.status_code == 200

        expected_result = [
            {
                "minute": "2023-09-01 18:32:00",
                "average_value": 6.51,
                "max_value": 9.43,
                "min_value": 3.64
            },
            {
                "minute": "2023-09-01 18:33:00",
                "average_value": 6.27,
                "max_value": 9.49,
                "min_value": 1.59
            }
        ]

        assert response.json() == expected_result
