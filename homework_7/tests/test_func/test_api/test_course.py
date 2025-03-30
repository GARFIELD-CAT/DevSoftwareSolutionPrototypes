from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "query_data, need_login, expected_status, expected_result",
    [
        (
            {
                "name": "Тестовое имя курса",
            },
            False,
            HTTPStatus.UNAUTHORIZED,
            {"detail": "Пользователь неавторизован"},
        ),
        (
            {
                "name": "Тестовое имя курса",
            },
            True,
            HTTPStatus.CREATED,
            {"id": 1, "name": "Тестовое имя курса"},
        ),
        (
            {
                "name": "qweqeq",
            },
            True,
            HTTPStatus.UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "ctx": {"error": {}},
                        "input": "qweqeq",
                        "loc": ["body", "name"],
                        "msg": "Value error, Название курса должно начинаться с большой "  # noqa: 501
                        "буквы и содержать только кирилицу/пробелы",
                        "type": "value_error",
                    }
                ]
            },
        ),
    ],
    ids=[
        "failed create course: user unauthorized",
        "succeed create course",
        "failed create course: bad input data",
    ],
)
@pytest.mark.asyncio()
async def test_create_course(
    app_client, query_data, need_login, expected_status, expected_result
):
    req_url = "/api/v1/courses/create_course/"

    if need_login:
        app_client.post(
            "/api/v1/auth/register/",
            json={
                "last_name": "Фамилия",
                "first_name": "Имя",
                "login": "test_login1",
                "email": "test@gmail.com",
                "password": "test_pass1",
            },
        )
        app_client.post(
            "/api/v1/auth/login/",
            json={
                "login": "test_login1",
                "password": "test_pass1",
            },
        )

    response = app_client.post(
        req_url,
        json=query_data,
    )
    result = response.json()

    assert response.status_code == expected_status
    assert result == expected_result


@pytest.mark.parametrize(
    "query_data, need_login, need_create_course, expected_status, expected_result",
    [
        (
            {
                "name": "Тестовое имя курса",
            },
            False,
            False,
            HTTPStatus.UNAUTHORIZED,
            {"detail": "Пользователь неавторизован"},
        ),
        (
            {
                "name": "Новое имя курса",
            },
            True,
            True,
            HTTPStatus.OK,
            {"message": "Course updated successfully", "status": "success"},
        ),
        (
            {
                "name": "Новое имя курса",
            },
            True,
            False,
            HTTPStatus.NOT_FOUND,
            {"detail": "Course not found"},
        ),
    ],
    ids=[
        "failed update course: user unauthorized",
        "succeed update course",
        "failed update course: course not found",
    ],
)
@pytest.mark.asyncio()
async def test_update_course(
    app_client,
    query_data,
    need_login,
    need_create_course,
    expected_status,
    expected_result,
):
    req_url = "/api/v1/courses/update_course/1"

    app_client.post(
        "/api/v1/courses/create_course/",
        json={
            "name": "Тестовое имя курса",
        },
    )

    if need_login:
        app_client.post(
            "/api/v1/auth/register/",
            json={
                "last_name": "Фамилия",
                "first_name": "Имя",
                "login": "test_login1",
                "email": "test@gmail.com",
                "password": "test_pass1",
            },
        )
        app_client.post(
            "/api/v1/auth/login/",
            json={
                "login": "test_login1",
                "password": "test_pass1",
            },
        )

    if need_create_course:
        app_client.post(
            "/api/v1/courses/create_course/",
            json={
                "name": "Тестовое имя курса",
            },
        )

    response = app_client.patch(
        req_url,
        json=query_data,
    )
    result = response.json()

    assert response.status_code == expected_status
    assert result == expected_result
