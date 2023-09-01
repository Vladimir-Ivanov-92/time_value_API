from pydantic import BaseModel


class AggregatedDataShow(BaseModel):
    minute: str
    average_value: float
    max_value: float
    min_value: float
