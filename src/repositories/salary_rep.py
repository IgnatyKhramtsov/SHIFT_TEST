from salary.models import Salary
from utils.repository import SQLAlchemySalaryRepository


class SalaryRepository(SQLAlchemySalaryRepository):
    model = Salary
