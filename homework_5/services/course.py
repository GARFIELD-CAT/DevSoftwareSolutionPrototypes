from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from homework_5.db.models.models import Course
from homework_5.services.entities import OperationStatus
from homework_5.services.main_service import MainService


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
            await db.rollback()
            if isinstance(e, IntegrityError):
                # SQLITE_CONSTRAINT_UNIQUE ERROR
                if e.orig.sqlite_errorcode == 2067:
                    return OperationStatus(
                        status="error", message="Курс с таким названием уже создан"
                    )

            return OperationStatus(
                status="error", message=f"Ошибка при создании курса: {e}"
            )

    async def get_course(self, course_id: int) -> Optional[Course]:
        session = self._get_async_session()

        async with session() as db:
            course = await db.execute(select(Course).where(Course.id == course_id))

            return course.scalars().one_or_none()

    async def delete_course(self, course_id: int) -> OperationStatus:
        session = self._get_async_session()

        async with session() as db:
            result = await db.execute(delete(Course).where(Course.id == course_id))

            await db.commit()

            if result.rowcount > 0:
                return OperationStatus(
                    status="success", message="Course deleted successfully"
                )
            else:
                return OperationStatus(status="error", message="Course not found")

    async def update_course(self, course_id: int, **kwargs) -> OperationStatus:
        session = self._get_async_session()

        async with session() as db:
            course = await db.execute(select(Course).where(Course.id == course_id))

            course = course.scalars().one_or_none()

            if course is None:
                return OperationStatus(status="error", message="Course not found")

            for key, value in kwargs.items():
                setattr(course, key, value)

            await db.commit()

            return OperationStatus(
                status="success", message="Course updated successfully"
            )

    async def get_unique_courses(self):
        session = self._get_async_session()

        async with session() as db:
            courses = await db.execute(select(Course))

            return courses.scalars().all()


course_service = CourseService()
