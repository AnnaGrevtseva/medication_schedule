from datetime import date, datetime
from pydantic import BaseModel
from typing import List


class ReceptionScheduleResponse(BaseModel):
    drug_name: str
    reception_frequency: int
    treatment_period: date
    reception_schedule: List[datetime]
