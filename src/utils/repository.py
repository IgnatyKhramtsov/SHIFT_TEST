from typing import Optional

from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession

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
        # async with async_session_maker() as session:
        stmt = select(self.model).where(
            func.lower(self.model.email) == func.lower(email)
        )
        result = await session.execute(stmt)
        result = result.unique().scalar_one_or_none()
        # result_dto = UserInDB.model_validate(result, from_attributes=True)
        return result
