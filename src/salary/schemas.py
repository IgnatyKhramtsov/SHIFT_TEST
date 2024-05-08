import uuid
from datetime import datetime

from pydantic import BaseModel


class SalaryCreate(BaseModel):
    title: int
    promotion_date: datetime
    user_id: uuid.UUID


class SalaryRead(SalaryCreate):
    id: int
