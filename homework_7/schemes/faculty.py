import re

from pydantic import BaseModel, Field, field_validator


class Faculty(BaseModel):
    name: str = Field(description="Название факультета")

    @field_validator("name", mode="before")
    def validate_name(cls, value):
        pattern = r"^[А-ЯЁ][а-яё\s]+$"
        if not re.match(pattern, value):
            raise ValueError(
                "Название факультета должно начинаться с большой буквы "
                "и содержать только кирилицу/пробелы"
            )

        return value


class ResponseFaculty(BaseModel):
    id: int = Field(description="Id факультета")
    name: str = Field(description="Название факультета")
