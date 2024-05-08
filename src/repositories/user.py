from user_auth.models import User
from utils.repository import SQLAlchemyUserRepository


class UserRepository(SQLAlchemyUserRepository):
    model = User
