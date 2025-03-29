import csv
from typing import Optional, Union

from sqlalchemy import func, select, delete

from homework_4.db.models.models import Course, Faculty, Student
from homework_4.services.course import course_service
from homework_4.services.entities import OperationStatus
from homework_4.services.faculty import faculty_service
from homework_4.services.main_service import MainService


class StudentService(MainService):
    async def load_from_csv(self, csv_filename="students.csv"):
        with open(csv_filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                try:
                    grade = int(row["Оценка"])
                except ValueError:
                    grade = 0

                await self.create_student(
                    last_name=row["Фамилия"],
                    first_name=row["Имя"],
                    faculty_name=row["Факультет"],
                    course_name=row["Курс"],
                    grade=grade,
                )

        print(f"Данные успешно загружены из csv файла {csv_filename}")

    async def create_student(
        self, last_name: str, first_name: str, faculty_id: int, course_id: int, grade: Optional[Union[int, float]]
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
            print(f"Ошибка при создании студента: {e}")
            await db.rollback()

        return None

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

        async with (session() as db):
            result = await db.execute(delete(Student).where(Student.id == student_id))

            await db.commit()

            if result.rowcount > 0:
                return OperationStatus(status='success', message='Student deleted successfully')
            else:
                return OperationStatus(status='error', message='Student not found')

    async def update_student(self, student_id: int, **kwargs) -> OperationStatus:
        session = self._get_async_session()

        async with (session() as db):
            student = await db.execute(select(Student).where(Student.id == student_id))

            student = student.scalars().one_or_none()

            if student is None:
                return OperationStatus(status='error', message='Student not found')

            faculty_id = kwargs.get('faculty_id', None)

            if faculty_id:
                faculty = await faculty_service.get_faculty(faculty_id=faculty_id)

                if faculty is None:
                    return OperationStatus(status='error', message=f'Факультет с таким {faculty_id=} не найден')

            course_id = kwargs.get('course_id', None)

            if course_id:
                course = await course_service.get_course(course_id=course_id)

                if course is None:
                    return OperationStatus(
                        status='error',
                        message=f'Курс с таким {course_id=} не найден'
                    )

            for key, value in kwargs.items():
                setattr(student, key, value)

            await db.commit()

            return OperationStatus(status='success', message='Student updated successfully')

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

student_service = StudentService()
