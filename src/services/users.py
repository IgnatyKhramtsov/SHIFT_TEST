from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from user_auth.hasher import get_password_hash
from user_auth.models import User
from user_auth.schemas import UserCreate


class UserService:
    def __init__(self, project_repo):
        self.project_repo = project_repo()

    async def create_user(self, user: UserCreate, session: AsyncSession):
        # db_obj = self.project_repo.model_validate(
        #     data, update={"hashed_password": get_password_hash(data.password)}
        # )
        user_dict = user.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = get_password_hash(password)
        try:
            res = await self.project_repo.create_user(user_dict, session)
            return res
        except Exception:
            raise HTTPException(status_code=422, detail="Incorrect data")

    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        res = await self.project_repo._get_user_by_email(email, session)
        return res
