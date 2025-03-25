import re
from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator


class Request(BaseModel):
    first_name: str = Field(
        pattern=r"^[А-ЯЁ][а-яё]+$", max_length=100, description="Имя"
    )
    last_name: str = Field(max_length=100, description="Фамилия")
    birth_date: date = Field(description="Дата рождения")
    phone: str = Field(description="Номер телефона")
    email: str = Field(description="Email адрес")

    @field_validator("first_name", mode="before")
    def validate_first_name(cls, value):
        pattern = r"^[А-ЯЁ][а-яё]+$"
        if not re.match(pattern, value):
            raise ValueError(
                "Имя должно начинаться с большой буквы и содержать только кирилицу"
            )
        return value

    @field_validator("last_name", mode="before")
    def validate_last_name(cls, value):
        pattern = r"^[А-ЯЁ][а-яё]+$"
        if not re.match(pattern, value):
            raise ValueError(
                "Фамилия должа начинаться с большой буквы и содержать только кирилицу"
            )
        return value

    @field_validator("birth_date", mode="before")
    def validate_birth_date(cls, value):
        today = date.today()
        value = datetime.strptime(value, "%Y-%m-%d")
        age = (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )

        if age < 18 or age > 120:
            raise ValueError("Возраст должен быть в пределах от 18 до 120 лет.")
        return value

    @field_validator("phone", mode="before")
    def validate_phone(cls, value):
        pattern = r"^\+7+([0-9]){10,15}$"
        if not re.match(pattern, value):
            raise ValueError("Номер телефона должен быть в формате: +7XXXXXXXXXX")
        return value

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, value):
            raise ValueError("Некорректный адрес электронной почты.")
        return value
