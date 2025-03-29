from typing import Optional

from sqlalchemy import select

from homework_4.db.models.models import Faculty
from homework_4.services.main_service import MainService


class FacultyService(MainService):
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

faculty_service = FacultyService()
