# from datetime import timedelta
# from typing import Annotated
#
# import uvicorn
# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_login import LoginManager
# from fastapi_login.exceptions import InvalidCredentialsException
# from pydantic import EmailStr
#
# from config import ACCESS_TOKEN_EXPIRE_MINUTES
# from db import SessionDep
# from repositories.user import UserRepository
# from services.users import UserService
# from user_auth.auth_user import authenticate_user
# from user_auth.hasher import verify_password
# from user_auth.schemas import Token
# from user_auth.security import create_access_token
#
# app = FastAPI(
#     docs_url='/'
# )
#
# SECRET = "SECRET_AUTH"
# manager = LoginManager(SECRET, "/token")
#
#
# @manager.user_loader()
# async def get_user_by_email(
#         email: EmailStr,
#         session: SessionDep,
# ):
#     res = await UserService(UserRepository).get_user_by_email(email, session)
#     return res
#
#
#
# @app.post("/token")
# async def login_for_access_token(
#     session: SessionDep,
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ) -> Token:
#     user = await authenticate_user(form_data.username, form_data.password, session)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
#     access_token = create_access_token(
#         data={"sub": user.email},
#         expires_delta=access_token_expires,
#     )
#     return Token(access_token=access_token, token_type="bearer")
#
#
# @app.get("/protected")
# def protected_route(user=Depends(manager)):
#     return {"user": user}
#
#
#
# if __name__ == "__main__":
#     uvicorn.run(f"many:app", port=8001, reload=True)
#
#
#
#
#
#
#
#
#
