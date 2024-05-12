import asyncio
from datetime import date, timedelta
from random import randint

import os
import sys


sys.path.append(os.path.join(sys.path[0], 'src'))


from src.repositories.salary_rep import SalaryRepository
from src.salary.schemas import SalaryCreate
from src.services.salary_serv import SalaryService
from src.db import async_session_maker
from src.repositories.user import UserRepository
from src.services.users import UserService
from src.user_auth.schemas import UserCreate

users = [
    {
      "email": "Pavel@gmail.com",
      "password": "123"
    },
    {
      "email": "Julia@gmail.com",
      "password": "string"
    },
    {
      "email": "Vladimir@ya.ru",
      "password": "456"
    },
    {
      "email": "goha@yahoo.com",
      "password": "azino777"
    }
]


async def create_users():
    async with async_session_maker() as session:
        for user in users:
            user_in = UserCreate(**user)
            res_user = await UserService(UserRepository).create_user(user_in, session)
            salary_level = randint(80000, 120000)
            promotion_date = date.today() + timedelta(weeks=randint(1, 30))
            salary_data = SalaryCreate(salary_level=salary_level, promotion_date=promotion_date)
            await SalaryService(SalaryRepository).add_salary(salary_data, res_user.user_id, session)



# запуск программы, основанной на корутинах
asyncio.run(create_users())