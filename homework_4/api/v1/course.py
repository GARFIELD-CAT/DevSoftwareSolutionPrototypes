from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException

from homework_4.schemes.course import Course, ResponseCourse
from homework_4.services.course import course_service

course_router = APIRouter()


@course_router.post("/create_course/", status_code=HTTPStatus.CREATED)
async def create_course(input: Course):
    course = await course_service.create_course(
        name=input.name,
    )

    return course


@course_router.get("/get_course/{id}", status_code=HTTPStatus.OK)
async def get_course(id: int):
    result = await course_service.get_course(id)

    if result is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return result


@course_router.delete("/delete_course/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_course(id: int):
    result = await course_service.delete_course(id)

    if result.status == "error":
        raise HTTPException(status_code=404, detail=result.message)

    return result


@course_router.patch("/update_course/{id}", status_code=HTTPStatus.OK)
async def update_course(id: int, input: Course):
    result = await course_service.update_course(id, **input.model_dump())

    if result.status == "error":
        raise HTTPException(status_code=404, detail=result.message)

    return result


@course_router.get(
    "/get_courses/", status_code=HTTPStatus.OK, response_model=List[ResponseCourse]
)
async def get_courses():
    return await course_service.get_unique_courses()
