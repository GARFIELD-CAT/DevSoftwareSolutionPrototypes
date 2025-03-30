import re

from pydantic import BaseModel, Field, field_validator


class Course(BaseModel):
    name: str = Field(description="Название курса")

    @field_validator("name", mode="before")
    def validate_name(cls, value):
        pattern = r"^[А-ЯЁ][а-яё\s]+$"
        if not re.match(pattern, value):
            raise ValueError(
                "Название курса должно начинаться с большой буквы "
                "и содержать только кирилицу/пробелы"
            )

        return value


class ResponseCourse(BaseModel):
    id: int = Field(description="Id курса")
    name: str = Field(description="Название курса")
