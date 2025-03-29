from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
