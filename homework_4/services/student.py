import csv

from sqlalchemy import func, select

from homework_4.db.models.models import Course, Faculty, Student
from homework_4.services.course import course_service
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
        self, last_name, first_name, faculty_name, course_name, grade
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
                else:
                    print(
                        f"Не удалось создать/найти факультет {faculty_name} или курс {course_name}"
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