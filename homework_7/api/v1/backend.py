import os
from http import HTTPStatus
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from homework_7.schemes.backend import ItemList
from homework_7.services.course import course_service
from homework_7.services.faculty import faculty_service
from homework_7.services.student import student_service
from homework_7.services.token import token_service

backend_router = APIRouter()

ACCESS_TOKEN_COOKIE_NAME = "access_token"
DB_DELETE_FUNC_FOR_TABLE_NAMES = {
    "faculties": faculty_service.delete_faculty,
    "courses": course_service.delete_course,
    "students": student_service.delete_student,
}


@backend_router.post("/fill_db/", status_code=HTTPStatus.OK)
async def fill_db(
    csv_file_path: str,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(token_service.get_auth_cookie),
):
    file_path = Path(__file__).parent.parent.parent / csv_file_path

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Файл {csv_file_path} не найден.",
        )

    background_tasks.add_task(student_service.load_from_csv, csv_file_path)

    return {"result": "ok"}


@backend_router.post("/remove_data_from_db/", status_code=HTTPStatus.OK)
async def remove_data_from_db(
    table_name: str,
    input: ItemList,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(token_service.get_auth_cookie),
):
    delete_func = DB_DELETE_FUNC_FOR_TABLE_NAMES.get(table_name, None)

    if delete_func is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Таблица с именем {table_name} не найдена.",
        )

    for item_id in input.item_ids:
        background_tasks.add_task(delete_func, item_id)

    return {"result": "ok"}
