from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer

from src.database import Base


class Value(Base):
    """
    Создается таблица value в БД
    """
    __tablename__ = "value"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow)
    value = Column(Float)


class TriggerTime(Base):
    """
    Создается таблица trigger_time в БД
    """
    __tablename__ = "trigger_time"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow)
