from datetime import UTC, datetime, timedelta
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response

from homework_5.schemes.user import AuthUser, User
from homework_5.services.password import password_service
from homework_5.services.token import token_service
from homework_5.services.user import user_service

auth_router = APIRouter()

ACCESS_TOKEN_COOKIE_NAME = "access_token"


@auth_router.post("/registration/", status_code=HTTPStatus.OK)
async def registration(input: User):
    hashed_password = password_service.create_hashed_password(input.password)

    user = await user_service.create_user(
        last_name=input.last_name,
        first_name=input.first_name,
        login=input.login,
        email=input.email,
        password=hashed_password,
    )

    return user


@auth_router.post("/login/", status_code=HTTPStatus.OK)
async def login(input: AuthUser, resp: Response):
    user = await user_service.get_user(user_login=input.login)

    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Неверный логин")

    is_valid = password_service.verify_password(input.password, user.password)

    if not is_valid:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Неверный пароль"
        )

    exp_time = datetime.now(UTC) + timedelta(minutes=120)
    token_data = {"login": user.login, "exp": exp_time, "type": "access"}
    token = token_service.create_token(token_data)

    resp.set_cookie(key=ACCESS_TOKEN_COOKIE_NAME, value=token, expires=exp_time)

    return {"status": "ok"}


@auth_router.post("/logout/", status_code=HTTPStatus.OK)
async def logout(resp: Response):
    resp.set_cookie(key=ACCESS_TOKEN_COOKIE_NAME, value="", expires=0)

    return {"status": "ok"}
