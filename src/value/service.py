from typing import Sequence

from fastapi import Depends
from sqlalchemy import Row, text
from sqlalchemy.engine.result import _TP
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.value.sql_text import minute_aggregated_sql


async def get_aggregated_data_from_db(
        session: AsyncSession = Depends(get_async_session)) -> Sequence[Row[_TP]]:
    """
    Обращается к БД используя SQL запрос и возвращает данные
    в виде списка объектов AggregatedDataShow
    """

    result = await session.execute(text(minute_aggregated_sql))
    minute_aggregated_data: Sequence[Row[_TP]] = result.fetchall()

    return minute_aggregated_data
