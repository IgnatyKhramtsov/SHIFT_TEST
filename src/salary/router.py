from typing import Annotated

from fastapi import APIRouter, Depends

from db import SessionDep
from repositories.salary_rep import SalaryRepository
from salary.schemas import SalaryCreate, SalaryRead
from services.salary_serv import SalaryService
from user_auth.auth_user import get_current_user
from user_auth.models import User

router = APIRouter(
    prefix="/api/v1/salaries",
    tags=["Salaries"]
)


# @router.post("/salary")
# async def add_salary_for_user(
#         salary_data: SalaryCreate,
#         session: SessionDep,
#         current_user: Annotated[User, Depends(get_current_user)]
# ):
#     res = await SalaryService(SalaryRepository).add_salary(salary_data, current_user.user_id, session)
#     return res


@router.get("/salary")
async def get_user_salary(
        session: SessionDep,
        current_user: Annotated[User, Depends(get_current_user)]
) -> SalaryRead:
    """
    ### Авторизуйтесь под своим Email'ом.
    ### Эндпоинт позволяет получить текущую зарплату и дату следующего повышения, текущего авторизованного пользователя.
    """
    res = await SalaryService(SalaryRepository).get_salary(current_user.user_id, session)
    return res
