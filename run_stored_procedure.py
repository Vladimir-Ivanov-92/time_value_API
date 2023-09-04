import asyncio
from datetime import datetime, timedelta

from sqlalchemy import text

from src.database import async_session_maker


async def add_value_at_intervals(interval_in_sec: int, run_time_in_minutes: int):
    """
    Выполняет хранимую процедуру. В параметрах задается время работы функции и интервал
    добавления данных в таблицу 'value'
    """
    end_time: datetime = datetime.now() + timedelta(minutes=run_time_in_minutes)

    while datetime.now() < end_time:
        async with async_session_maker() as session:
            # Определяем SQL-запрос для вызова хранимой процедуры
            sql: str = "SELECT insert_random_value()"

            # Выполняем SQL-запрос с использованием сессии
            await session.execute(text(sql))
            await session.commit()
            print("Значение добавлено в таблицу")

            remaining_time: timedelta = end_time - datetime.now()
            print(f"Оставшееся время работы: {remaining_time}")

            await asyncio.sleep(interval_in_sec)


if __name__ == '__main__':
    # Асинхронный вызов процедуры
    asyncio.run(add_value_at_intervals(interval_in_sec=5, run_time_in_minutes=1))
