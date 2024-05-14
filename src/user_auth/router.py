from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from db import SessionDep
from repositories.user import UserRepository
from services.users import UserService
from user_auth.auth_user import get_current_user
from user_auth.models import User
from user_auth.schemas import UserCreate, UserRead

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post("",
             summary="Создает нового пользователя",
             status_code=201
             )
async def create_user(
        user_in: UserCreate,
        session: SessionDep
):
    """
    ## Создает нового пользователя
    ### - **email [str]**: Email нового пользователя
    ### - **password [str]**: Пароль нового пользователя

    """
    user = await UserService(UserRepository).get_user_by_email(email=user_in.email, session=session)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    res = await UserService(UserRepository).create_user(user_in, session)
    result = jsonable_encoder(res)
    return JSONResponse(content=result, status_code=HTTP_201_CREATED)


@router.get("", response_model=UserRead)
async def get_user_by_email(
        email: EmailStr,
        session: SessionDep,
        current_user: Annotated[User, Depends(get_current_user)]
):
    res = await UserService(UserRepository).get_user_by_email(email, session)
    return res
