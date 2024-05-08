from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.db import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class Salary(Base):
    __tablename__ = "salary"

    id: Mapped[intpk]
    salary: Mapped[int]
    promotion_date: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now() + INTERVAL '6 months')")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)
