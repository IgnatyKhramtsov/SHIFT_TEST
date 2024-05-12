import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from salary.schemas import SalaryCreateUUID, SalaryCreate
from user_auth.models import User


class SalaryService:
    def __init__(self, project_repo):
        self.project_repo = project_repo()

    async def add_salary(self, salary_data: SalaryCreate, user: uuid.UUID, session: AsyncSession):
        salary_data = SalaryCreateUUID(**salary_data.model_dump(), user_id=user)
        salary_dict = salary_data.model_dump()
        try:
            res = await self.project_repo.add_salary_level(salary_dict, session)
            return res
        except Exception:
            raise HTTPException(status_code=422, detail="Incorrect data")

    async def get_salary(self, user_id: uuid.UUID, session: AsyncSession):
        result = await self.project_repo.get_salary(user_id, session)
        return result
