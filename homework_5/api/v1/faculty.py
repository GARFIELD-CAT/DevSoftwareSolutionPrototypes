from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from homework_5.schemes.faculty import Faculty, ResponseFaculty
from homework_5.services.faculty import faculty_service
from homework_5.services.token import token_service

faculty_router = APIRouter()


@faculty_router.post("/create_faculty/", status_code=HTTPStatus.CREATED)
async def create_faculty(
    input: Faculty, current_user: str = Depends(token_service.get_auth_cookie)
):
    faculty = await faculty_service.create_faculty(
        name=input.name,
    )

    return faculty


@faculty_router.get("/get_faculty/{id}", status_code=HTTPStatus.OK)
async def get_faculty(
    id: int, current_user: str = Depends(token_service.get_auth_cookie)
):
    result = await faculty_service.get_faculty(id)

    if result is None:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return result


@faculty_router.delete("/delete_faculty/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_faculty(
    id: int, current_user: str = Depends(token_service.get_auth_cookie)
):
    result = await faculty_service.delete_faculty(id)

    if result.status == "error":
        raise HTTPException(status_code=404, detail=result.message)

    return result


@faculty_router.patch("/update_faculty/{id}", status_code=HTTPStatus.OK)
async def update_faculty(
    id: int, input: Faculty, current_user: str = Depends(token_service.get_auth_cookie)
):
    result = await faculty_service.update_faculty(id, **input.model_dump())

    if result.status == "error":
        raise HTTPException(status_code=404, detail=result.message)

    return result


@faculty_router.get(
    "/get_faculties/", status_code=HTTPStatus.OK, response_model=List[ResponseFaculty]
)
async def get_faculties(current_user: str = Depends(token_service.get_auth_cookie)):
    return await faculty_service.get_unique_faculties()
