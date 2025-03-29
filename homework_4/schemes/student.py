from pydantic import BaseModel, Field, model_validator, field_validator


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
        elif  value < 0:
            raise ValueError("Оценка не может быть меньше 0")

        return value

    # @model_validator(mode="before")
    # def validate_last_name(self):
    #     ...