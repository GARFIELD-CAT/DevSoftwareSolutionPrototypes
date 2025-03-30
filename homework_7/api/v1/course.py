import json
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from homework_7.schemes.course import Course, ResponseCourse
from homework_7.services.course import course_service
from homework_7.services.token import token_service
from homework_7.storages.cache import cache_storage

course_router = APIRouter()
COURSE_CACHE_PREFIX_KEY = "course"


@course_router.post("/create_course/", status_code=HTTPStatus.CREATED)
async def create_course(
    input: Course, current_user: str = Depends(token_service.get_auth_cookie)
):
    course = await course_service.create_course(
        name=input.name,
    )

    return course


@course_router.get("/get_course/{id}", status_code=HTTPStatus.OK)
async def get_course(
    id: int, current_user: str = Depends(token_service.get_auth_cookie)
):
    course = await cache_storage.get(f"{COURSE_CACHE_PREFIX_KEY}:{id}")

    if course:
        return json.loads(course)
    else:
        course = await course_service.get_course(id)

        if course is None:
            raise HTTPException(status_code=404, detail="Course not found")

        await cache_storage.set(
            f"{COURSE_CACHE_PREFIX_KEY}:{id}", json.dumps(course.as_dict())
        )

    return course


@course_router.delete("/delete_course/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_course(
    id: int, current_user: str = Depends(token_service.get_auth_cookie)
):
    result = await course_service.delete_course(id)

    if result.status == "error":
        raise HTTPException(status_code=404, detail=result.message)

    await cache_storage.delete(f"{COURSE_CACHE_PREFIX_KEY}:{id}")

    return result


@course_router.patch("/update_course/{id}", status_code=HTTPStatus.OK)
async def update_course(
    id: int, input: Course, current_user: str = Depends(token_service.get_auth_cookie)
):
    result = await course_service.update_course(id, **input.model_dump())

    if result.status == "error":
        raise HTTPException(status_code=404, detail=result.message)

    await cache_storage.delete(f"{COURSE_CACHE_PREFIX_KEY}:{id}")

    return result


@course_router.get(
    "/get_courses/", status_code=HTTPStatus.OK, response_model=List[ResponseCourse]
)
async def get_courses(current_user: str = Depends(token_service.get_auth_cookie)):
    return await course_service.get_unique_courses()
