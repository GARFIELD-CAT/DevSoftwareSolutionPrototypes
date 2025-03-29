from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from homework_4.schemes.student import Student
from homework_4.services.student import student_service

student_router = APIRouter()


@student_router.post("/create_student/", status_code=HTTPStatus.CREATED)
async def create_student(input: Student):
    student = await student_service.create_student(
        last_name=input.last_name,
        first_name=input.first_name,
        faculty_id=input.faculty_id,
        course_id=input.course_id,
        grade=input.grade,
    )

    return student

@student_router.get(
    "/get_student/{id}",
    status_code=HTTPStatus.OK
)
async def get_student(id: int):
    result = await student_service.get_student(id)

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return result

@student_router.delete("/delete_student/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_student(id: int):
    result = await student_service.delete_student(id)

    if result.status == 'error':
        raise HTTPException(status_code=404, detail=result.message)

    return result

@student_router.patch("/update_student/{id}", status_code=HTTPStatus.OK)
async def update_student(id: int, input: Student):
    result = await student_service.update_student(id, **input.model_dump())

    if result.status == 'error':
        raise HTTPException(status_code=404, detail=result.message)

    return result

@student_router.get("/get_students/", status_code=HTTPStatus.OK)
async def get_students():
    return await student_service.get_students()
