from datetime import datetime, date
from typing import Annotated
from sqlalchemy import ForeignKey, text
from user_auth.models import *
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from db import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class Salary(Base):
    __tablename__ = "salary"

    id: Mapped[intpk]
    salary_level: Mapped[int]
    promotion_date: Mapped[date] = mapped_column(nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)
