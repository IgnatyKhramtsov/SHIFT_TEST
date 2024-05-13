import asyncio
from datetime import timedelta, date
from random import randint
from typing import AsyncGenerator

import pytest
from fastapi import Depends
from httpx import AsyncClient, ASGITransport
from pytest_asyncio import is_async_test
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db import Base, get_async_session, SessionDep
from repositories.salary_rep import SalaryRepository
from repositories.user import UserRepository
from salary.schemas import SalaryCreate
from services.salary_serv import SalaryService
from services.users import UserService
from src.config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST, ACCESS_TOKEN_EXPIRE_MINUTES
from src.main import app
from src.user_auth.security import create_access_token
from user_auth.schemas import UserCreate

DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, echo=False)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# from alembic import command
# from alembic.config import Config
#
# @pytest.fixture(autouse=True, scope="session")
# def prepare_database():
#     alembic_cfg = Config("alembic.ini")
#     alembic_cfg.set_main_option(
#         "sqlalchemy.url",
#         f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}?async_fallback=True"
#     )
#     command.upgrade(alembic_cfg, "head")
#     yield
#     command.downgrade(alembic_cfg, "base")


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


transport = ASGITransport(app=app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def create_user_salary_in_database(user: dict):
    async with async_session_maker() as session:
        user_in = UserCreate(**user)
        res_user = await UserService(UserRepository).create_user(user_in, session)
        salary_level = randint(80000, 120000)
        promotion_date = date.today() + timedelta(weeks=randint(1, 30))
        salary_data = SalaryCreate(salary_level=salary_level, promotion_date=promotion_date)
        await SalaryService(SalaryRepository).add_salary(salary_data, res_user.user_id, session)



def create_test_auth_headers_for_user(email: str) -> dict[str, str]:
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    return {"Authorization": f"Bearer {access_token}"}
