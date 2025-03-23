from datetime import date

from pydantic import BaseModel, Field


class Schedule(BaseModel):
    drug_name: str
    reception_frequency: int = Field(default=1)
    treatment_period: date
    user_id: int = Field(default=1)
