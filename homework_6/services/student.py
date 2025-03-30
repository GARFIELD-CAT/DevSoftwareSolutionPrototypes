import csv
from pathlib import Path
from typing import Optional, Union

from sqlalchemy import delete, func, select

from homework_6.db.models.models import Course, Faculty, Student
from homework_6.services.course import course_service
from homework_6.services.entities import OperationStatus
from homework_6.services.faculty import faculty_service
from homework_6.services.main_service import MainService

DEFAULT_CSV_FILE_PATH = Path(__file__).parent.parent / "db/init_data/students.csv"


class StudentService(MainService):
    async def load_from_csv(self, csv_file_path: str = DEFAULT_CSV_FILE_PATH):
        with open(csv_file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    grade = int(row["Оценка"])
                except ValueError:
                    grade = 0

                await self._create_student_from_csv(
                    last_name=row["Фамилия"],
                    first_name=row["Имя"],
                    faculty_name=row["Факультет"],
                    course_name=row["Курс"],
                    grade=grade,
                )

        print(f"Данные успешно загружены из csv файла {csv_file_path}")

    async def create_student(
        self,
        last_name: str,
        first_name: str,
        grade: Optional[Union[int, float]],
        faculty_id: int,
        course_id: int,
    ):
        session = self._get_async_session()

        try:
            async with session() as db:
                faculty = await faculty_service.get_faculty(faculty_id=faculty_id)

                if faculty is None:
                    raise ValueError(f"Факультет с таким {faculty_id=} не найден")

                course = await course_service.get_course(course_id=course_id)

                if course is None:
                    raise ValueError(f"Курс с таким {course_id=} не найден")

                if faculty and course:
                    student = Student(
                        last_name=last_name,
                        first_name=first_name,
                        faculty=faculty.id,
                        course=course.id,
                        grade=grade,
                    )
                    db.add(student)
                    await db.commit()

                return student
        except Exception as e:
            await db.rollback()

            return OperationStatus(
                status="error", message=f"Ошибка при создании студента: {e}"
            )

    async def get_student(self, student_id: int):
        session = self._get_async_session()

        async with session() as db:
            student = await db.execute(select(Student).where(Student.id == student_id))

            return student.scalars().one_or_none()

    async def get_students(self):
        session = self._get_async_session()

        async with session() as db:
            students = await db.execute(select(Student))

            return students.scalars().all()

    async def delete_student(self, student_id: int) -> OperationStatus:
        session = self._get_async_session()

        async with session() as db:
            result = await db.execute(delete(Student).where(Student.id == student_id))

            await db.commit()

            if result.rowcount > 0:
                print(f"success: Student {student_id=} deleted successfully")
                return OperationStatus(
                    status="success", message="Student deleted successfully"
                )
            else:
                print(f"error: Student {student_id=} not found")
                return OperationStatus(status="error", message="Student not found")

    async def update_student(self, student_id: int, **kwargs) -> OperationStatus:
        session = self._get_async_session()

        async with session() as db:
            student = await db.execute(select(Student).where(Student.id == student_id))

            student = student.scalars().one_or_none()

            if student is None:
                return OperationStatus(status="error", message="Student not found")

            faculty_id = kwargs.get("faculty_id", None)

            if faculty_id:
                faculty = await faculty_service.get_faculty(faculty_id=faculty_id)

                if faculty is None:
                    return OperationStatus(
                        status="error",
                        message=f"Факультет с таким {faculty_id=} не найден",
                    )

            course_id = kwargs.get("course_id", None)

            if course_id:
                course = await course_service.get_course(course_id=course_id)

                if course is None:
                    return OperationStatus(
                        status="error", message=f"Курс с таким {course_id=} не найден"
                    )

            for key, value in kwargs.items():
                if value:
                    setattr(student, key, value)

            await db.commit()

            return OperationStatus(
                status="success", message="Student updated successfully"
            )

    async def get_average_students_grade_by_faculty(self, faculty_name: str):
        session = self._get_async_session()

        async with session() as db:
            avg_grade = await db.execute(
                select(func.avg(Student.grade))
                .join(Faculty)
                .filter(Faculty.name == faculty_name)
            )

            return avg_grade.scalars().one()

    async def get_students_by_faculty(self, faculty_name: str):
        session = self._get_async_session()

        async with session() as db:
            students = await db.execute(
                select(Student).join(Faculty).filter(Faculty.name == faculty_name)
            )

            return students.scalars().all()

    async def get_students_below_grade_by_course(
        self, course_name: str, max_grade: int = 30
    ):
        session = self._get_async_session()

        async with session() as db:
            students = await db.execute(
                select(Student)
                .join(Course)
                .filter(Course.name == course_name, Student.grade < max_grade)
            )

            return students.scalars().all()

    async def _create_student_from_csv(
        self,
        last_name: str,
        first_name: str,
        grade: Optional[Union[int, float]],
        faculty_name: Optional[str] = None,
        course_name: Optional[str] = None,
    ):
        session = self._get_async_session()

        try:
            async with session() as db:
                faculty = await faculty_service.get_faculty(faculty_name=faculty_name)

                if faculty is None:
                    faculty = await faculty_service.create_faculty(faculty_name)

                course = await course_service.get_course(course_name=course_name)

                if course is None:
                    course = await course_service.create_course(course_name)

                if faculty and course:
                    student = Student(
                        last_name=last_name,
                        first_name=first_name,
                        faculty=faculty.id,
                        course=course.id,
                        grade=grade,
                    )
                    db.add(student)
                    await db.commit()

                return student
        except Exception as e:
            await db.rollback()

            return OperationStatus(
                status="error", message=f"Ошибка при создании студента: {e}"
            )


student_service = StudentService()
