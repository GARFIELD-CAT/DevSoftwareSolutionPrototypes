import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BaseUser(BaseModel):
    last_name: str = Field(description="Фамилия")
    first_name: str = Field(description="Имя")
    login: str = Field(description="Логин")
    email: str = Field(description="Email")
    password: str = Field(description="Пароль")

    @field_validator("last_name", mode="before")
    def validate_last_name(cls, value):
        pattern = r"^[А-ЯЁ][а-яё]+$"
        if not re.match(pattern, value):
            raise ValueError(
                "Фамилия должна начинаться с большой буквы и содержать только кирилицу"
            )

        return value

    @field_validator("first_name", mode="before")
    def validate_first_name(cls, value):
        pattern = r"^[А-ЯЁ][а-яё]+$"
        if not re.match(pattern, value):
            raise ValueError(
                "Имя должно начинаться с большой буквы и содержать только кирилицу"
            )

        return value

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, value):
            raise ValueError("Некорректный адрес электронной почты.")

        return value


class User(BaseUser):
    last_name: str = Field(description="Фамилия")
    first_name: str = Field(description="Имя")
    login: str = Field(description="Логин")
    email: str = Field(description="Email")
    password: str = Field(description="Пароль")


class UpdateUser(BaseUser):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    login: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class AuthUser(BaseModel):
    login: str = Field(description="Логин")
    password: str = Field(description="Пароль")
