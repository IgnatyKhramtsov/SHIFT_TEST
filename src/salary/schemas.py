import uuid
from datetime import date

from pydantic import BaseModel


class SalaryCreate(BaseModel):
    salary_level: int
    promotion_date: date


class SalaryCreateUUID(SalaryCreate):
    user_id: uuid.UUID


class SalaryRead(SalaryCreateUUID):
    id: int
