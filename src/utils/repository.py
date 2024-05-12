import uuid
from typing import Optional

from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from salary.schemas import SalaryRead
from user_auth.models import User
from user_auth.schemas import UserRead


class SQLAlchemyUserRepository:
    model = None

    async def create_user(self, user_data, session: AsyncSession) -> UserRead:
        stmt = insert(self.model).values(**user_data).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        result_dto = UserRead.model_validate(res.scalar_one(), from_attributes=True)
        return result_dto

    async def _get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        stmt = select(self.model).where(
            func.lower(self.model.email) == func.lower(email)
        )
        result = await session.execute(stmt)
        result = result.unique().scalar_one_or_none()
        # result_dto = UserInDB.model_validate(result, from_attributes=True)
        return result


class SQLAlchemySalaryRepository:
    model = None

    async def add_salary_level(self, salary_data: dict, session: AsyncSession):
        stmt = insert(self.model).values(**salary_data).returning(self.model)
        result = await session.execute(stmt)
        await session.commit()
        result_dto = SalaryRead.model_validate(result.scalar_one(), from_attributes=True)
        return result_dto

    async def get_salary(self, user_id: uuid.UUID, session: AsyncSession):
        query = select(self.model).where(self.model.user_id == user_id)
        res = await session.execute(query)
        result = res.unique().scalars().all()
        result_dto = [SalaryRead.model_validate(row, from_attributes=True) for row in result]
        return result_dto
