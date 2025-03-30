from http import HTTPStatus

import pytest

from homework_7.services.password import password_service


@pytest.mark.parametrize(
    "query_data, expected_status, expected_result",
    [
        (
            {
                "last_name": "Фамилия",
                "first_name": "Имя",
                "login": "test_login",
                "email": "test@gmail.com",
                "password": "test_pass",
            },
            HTTPStatus.OK,
            {
                "id": 1,
                "last_name": "Фамилия",
                "first_name": "Имя",
                "login": "test_login",
                "email": "test@gmail.com",
            },
        ),
        (
            {
                "last_name": "Фамилия",
                "first_name": "Bad2",
                "login": "test_login",
                "email": "test@gmail.com",
                "password": "test_pass",
            },
            HTTPStatus.UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "first_name"],
                        "msg": "Value error, Имя должно начинаться с большой буквы и содержать только кирилицу",  # noqa: 501
                        "input": "Bad2",
                        "ctx": {"error": {}},
                    }
                ]
            },
        ),
    ],
    ids=[
        "succeed register user",
        "failed register: bad input data",
    ],
)
@pytest.mark.asyncio()
async def test_register(app_client, query_data, expected_status, expected_result):
    req_url = "/api/v1/auth/register/"

    response = app_client.post(
        req_url,
        json=query_data,
    )
    result = response.json()
    hashed_password = result.get("password", None)

    assert response.status_code == expected_status

    if hashed_password:
        result.pop("password")
        assert (
            password_service.verify_password(query_data["password"], hashed_password)
            is True
        )

    assert result == expected_result


@pytest.mark.parametrize(
    "query_data, expected_status, expected_result, cookie_added",
    [
        (
            {
                "login": "test_login1",
                "password": "test_pass1",
            },
            HTTPStatus.OK,
            {"status": "ok"},
            True,
        ),
        (
            {
                "login": "test_login2",
                "password": "test_pass2",
            },
            HTTPStatus.BAD_REQUEST,
            {"detail": "Неверный логин"},
            False,
        ),
        (
            {
                "login": "test_login1",
                "password": "test_pass2",
            },
            HTTPStatus.BAD_REQUEST,
            {"detail": "Неверный пароль"},
            False,
        ),
    ],
    ids=[
        "succeed login user",
        "failed login: unknown user",
        "failed login: wrong password",
    ],
)
@pytest.mark.asyncio()
async def test_login(
    app_client, query_data, expected_status, expected_result, cookie_added
):
    req_url = "/api/v1/auth/login/"

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

    response = app_client.post(
        req_url,
        json=query_data,
    )
    result = response.json()

    assert response.status_code == expected_status
    assert result == expected_result
    assert bool(response.cookies.get("access_token")) == cookie_added


@pytest.mark.parametrize(
    "expected_status, need_login, expected_result, has_cookie",
    [
        (
            HTTPStatus.OK,
            True,
            {"status": "ok"},
            False,
        ),
        (
            HTTPStatus.OK,
            False,
            {"status": "ok"},
            False,
        ),
    ],
    ids=[
        "succeed logout user with login",
        "succeed logout user without login",
    ],
)
@pytest.mark.asyncio()
async def test_logout(
    app_client, need_login, expected_status, expected_result, has_cookie
):
    req_url = "/api/v1/auth/logout/"

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

    if need_login:
        response = app_client.post(
            "/api/v1/auth/login/",
            json={
                "login": "test_login1",
                "password": "test_pass1",
            },
        )

        assert bool(response.cookies.get("access_token")) is True

    response = app_client.post(
        req_url,
    )
    result = response.json()

    assert response.status_code == expected_status
    assert result == expected_result
    assert bool(response.cookies.get("access_token")) == has_cookie
