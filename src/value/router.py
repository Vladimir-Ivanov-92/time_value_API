from typing import Sequence, Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Row
from sqlalchemy.engine.result import _TP
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from value.schemas import AggregatedDataShow
from value.service import get_aggregated_data_from_db

from typing import Optional

value_router = APIRouter(
    prefix="/value",
    tags=["value"],
)


@value_router.get("/agr", response_model=Optional[list[AggregatedDataShow]])
async def get_minute_aggregated_data(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> Optional[list[AggregatedDataShow]]:
    """
    Возвращает поминутно агрегированные данные таблицы 'value' если пользователь
    авторизирован
    """

    minute_aggregated_data: Sequence[Row[_TP]] = await get_aggregated_data_from_db(
        session)

    aggregated_data: list = []

    for row in minute_aggregated_data:
        minute: str = row[0].strftime(
            "%Y-%m-%d %H:%M:%S")  # Преобразование datetime в строку
        average_value: float = row[1]
        max_value: float = row[2]
        min_value: float = row[3]

        aggregated_data.append(AggregatedDataShow(
            minute=minute,
            average_value=average_value,
            max_value=max_value,
            min_value=min_value,
        ))

    return aggregated_data
