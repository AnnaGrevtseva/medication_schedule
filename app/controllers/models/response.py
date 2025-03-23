from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class ReceptionScheduleResponse(BaseModel):
    drug_name: str
    reception_frequency: int
    treatment_period: date
    reception_schedule: List[datetime]
