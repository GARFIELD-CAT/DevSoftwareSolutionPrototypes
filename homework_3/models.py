import re
from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Модели fast api для данных
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


# Модели базы данных
Base = declarative_base()


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    students = relationship("Student", back_populates="faculties", lazy="subquery")

    def __repr__(self):
        return f"{self.id} - {self.name}"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    students = relationship("Student", back_populates="courses", lazy="subquery")

    def __repr__(self):
        return f"{self.id} - {self.name}"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(128))
    first_name = Column(String(128))
    grade = Column(Integer)
    faculty = Column(Integer, ForeignKey("faculties.id", ondelete="CASCADE"))
    course = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))

    faculties = relationship("Faculty", back_populates="students", lazy="subquery")
    courses = relationship("Course", back_populates="students", lazy="subquery")

    def __repr__(self):
        return (
            f"{self.id} - {self.last_name} - {self.first_name} - "
            f"{self.grade} - {self.faculty} - {self.course}"
        )
