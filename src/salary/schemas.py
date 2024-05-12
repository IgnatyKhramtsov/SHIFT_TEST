import uuid
from datetime import datetime, timedelta, date

from pydantic import BaseModel


class SalaryCreate(BaseModel):
    salary_level: int
    promotion_date: date  #time.timestamp = (datetime.now() + timedelta(weeks=26)).timestamp()


class SalaryCreateUUID(SalaryCreate):
    user_id: uuid.UUID


class SalaryRead(SalaryCreateUUID):
    id: int
