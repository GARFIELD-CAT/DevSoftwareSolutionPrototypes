import csv
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from homework_3.models import Base, Course, Faculty, Student


class StudentManager:
    def __init__(self, db_url: str = "sqlite+aiosqlite:///./student.db"):
        self._db_url = db_url
        self._engine = create_async_engine(self._db_url)

    async def init_db(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_db(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

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

    def _get_async_session(self):
        return sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_faculty(self, name):
        session = self._get_async_session()

        faculty = Faculty(name=name)

        try:
            async with session() as db:
                db.add(faculty)
                await db.commit()

            return faculty
        except Exception as e:
            print(f"Ошибка при создании факультета: {e}")
            await db.rollback()

        return None

    async def create_course(self, name):
        session = self._get_async_session()

        course = Course(name=name)

        try:
            async with session() as db:
                db.add(course)
                await db.commit()

            return course
        except Exception as e:
            print(f"Ошибка при создании курса: {e}")
            await db.rollback()

        return None

    async def create_student(
        self, last_name, first_name, faculty_name, course_name, grade
    ):
        session = self._get_async_session()

        try:
            async with session() as db:
                faculty = await self.get_faculty(faculty_name=faculty_name)

                if faculty is None:
                    faculty = await self.create_faculty(faculty_name)

                course = await self.get_course(course_name=course_name)

                if course is None:
                    course = await self.create_course(course_name)

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
                else:
                    print(
                        f"Не удалось создать/найти факультет {faculty_name} "
                        f"или курс {course_name}"
                    )

            return student
        except Exception as e:
            print(f"Ошибка при создании студента: {e}")
            await db.rollback()

        return None

    async def get_student(self, student_id: int):
        session = self._get_async_session()

        async with session() as db:
            students = await db.execute(select(Student).where(Student.id == student_id))

            return students.scalars().one_or_none()

    async def get_faculty(
        self, faculty_id: Optional[int] = None, faculty_name: Optional[str] = None
    ) -> Optional[Faculty]:
        session = self._get_async_session()

        async with session() as db:
            if faculty_id:
                faculty = await db.execute(
                    select(Faculty).where(Faculty.id == faculty_id)
                )
            elif faculty_name:
                faculty = await db.execute(
                    select(Faculty).where(Faculty.name == faculty_name)
                )
            else:
                return None

            return faculty.scalars().one_or_none()

    async def get_course(
        self, course_id: Optional[int] = None, course_name: Optional[str] = None
    ) -> Optional[Course]:
        session = self._get_async_session()

        async with session() as db:
            if course_id:
                course = await db.execute(select(Course).where(Course.id == course_id))
            elif course_name:
                course = await db.execute(
                    select(Course).where(Course.name == course_name)
                )
            else:
                return None

            return course.scalars().one_or_none()

    async def get_students_by_faculty(self, faculty_name: str):
        session = self._get_async_session()

        async with session() as db:
            students = await db.execute(
                select(Student).join(Faculty).filter(Faculty.name == faculty_name)
            )

        return students.scalars().all()

    async def get_unique_courses(self):
        session = self._get_async_session()

        async with session() as db:
            courses = await db.execute(select(Course))

        return courses.scalars().all()

    async def get_average_grade_by_faculty(self, faculty_name: str):
        session = self._get_async_session()

        async with session() as db:
            avg_grade = await db.execute(
                select(func.avg(Student.grade))
                .join(Faculty)
                .filter(Faculty.name == faculty_name)
            )

        return avg_grade.scalars().one()

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
