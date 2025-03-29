from typing import Optional

from sqlalchemy import select

from homework_4.db.models.models import Course
from homework_4.services.main_service import MainService


class CourseService(MainService):
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

    async def get_unique_courses(self):
        session = self._get_async_session()

        async with session() as db:
            courses = await db.execute(select(Course))

        return courses.scalars().all()


course_service = CourseService()