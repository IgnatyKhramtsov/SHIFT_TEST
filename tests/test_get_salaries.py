from httpx import AsyncClient

from tests.conftest import create_test_auth_headers_for_user, create_user_salary_in_database


async def test_get_auth_user_salary_async(ac: AsyncClient):
    user = {
        "email": "Pavel123@gmail.com",
        "password": "123"
    }

    await create_user_salary_in_database(user)

    response = await ac.get('/api/v1/salaries/salary', headers=create_test_auth_headers_for_user(user["email"]))
    assert response.status_code == 200


async def test_get_not_auth_user_salary_async(ac: AsyncClient):

    response = await ac.get('/api/v1/salaries/salary')
    assert response.status_code == 401