from datetime import date, datetime
from typing import List, Tuple

from pydantic import BaseModel, Field


class ReceptionScheduleResponse(BaseModel):
    drug_name: str
    reception_frequency: int
    treatment_period: date
    reception_schedule: List[datetime]


class IdScheduleResponse(BaseModel):
    schedule_id: int = Field(default=1)


class IdsScheduleResponse(BaseModel):
    schedule_id_list: List[int]


class NextTakingsResponse(BaseModel):
    next_takings: List[Tuple]
