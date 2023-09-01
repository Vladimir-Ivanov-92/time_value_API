from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float

from src.database import Base


class Value(Base):
    __tablename__ = "value"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow)
    value = Column(Float)