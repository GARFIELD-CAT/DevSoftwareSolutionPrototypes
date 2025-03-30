import re

from pydantic import BaseModel, Field, field_validator


class Student(BaseModel):
    last_name: str = Field(description="Фамилия")
    first_name: str = Field(description="Имя")
    grade: int = Field(description="Оценка")
    faculty_id: int = Field(description="Факультет", default=1)
    course_id: int = Field(description="Курс", default=1)

    @field_validator("grade", mode="before")
    def validate_grade(cls, value):

        if value > 100:
            raise ValueError("Оценка не может превышать 100 баллов")
        elif value < 0:
            raise ValueError("Оценка не может быть меньше 0")

        return value

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
