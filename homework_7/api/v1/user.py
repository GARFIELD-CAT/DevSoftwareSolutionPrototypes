import json
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from homework_7.schemes.user import UpdateUser, User
from homework_7.services.password import password_service
from homework_7.services.token import token_service
from homework_7.services.user import user_service
from homework_7.storages.cache import cache_storage

user_router = APIRouter()
USER_CACHE_PREFIX_KEY = "user"


@user_router.post("/create_user/", status_code=HTTPStatus.CREATED)
async def create_user(
    input: User, current_user: str = Depends(token_service.get_auth_cookie)
):
    hashed_password = password_service.create_hashed_password(input.password)

    user = await user_service.create_user(
        last_name=input.last_name,
        first_name=input.first_name,
        login=input.login,
        email=input.email,
        password=hashed_password,
    )

    return user


@user_router.get("/get_user/{user_id}", status_code=HTTPStatus.OK)
async def get_user(
    user_id: int, current_user: str = Depends(token_service.get_auth_cookie)
):
    user = await cache_storage.get(f"{USER_CACHE_PREFIX_KEY}:{user_id}")

    if user:
        return json.loads(user)
    else:
        user = await user_service.get_user(user_id=user_id)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await cache_storage.set(
            f"{USER_CACHE_PREFIX_KEY}:{user_id}", json.dumps(user.as_dict())
        )

    return user


@user_router.delete("/delete_user/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(
    user_id: int, current_user: str = Depends(token_service.get_auth_cookie)
):
    result = await user_service.delete_user(user_id)

    if result.status == "error":
        raise HTTPException(status_code=404, detail=result.message)

    await cache_storage.delete(f"{USER_CACHE_PREFIX_KEY}:{user_id}")

    return result


@user_router.patch("/update_user/{user_id}", status_code=HTTPStatus.OK)
async def update_user(
    user_id: int,
    input: UpdateUser,
    current_user: str = Depends(token_service.get_auth_cookie),
):
    if input.password:
        input.password = password_service.create_hashed_password(input.password)

    result = await user_service.update_user(user_id, **input.model_dump())

    if result.status == "error":
        raise HTTPException(status_code=404, detail=result.message)

    await cache_storage.delete(f"{USER_CACHE_PREFIX_KEY}:{user_id}")

    return result
