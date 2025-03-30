from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from homework_7.db.models.models import User
from homework_7.services.entities import OperationStatus
from homework_7.services.main_service import MainService


class UserService(MainService):
    async def create_user(
        self,
        last_name: str,
        first_name: str,
        login: str,
        email: str,
        password: str,
    ):
        session = self._get_async_session()

        user = User(
            last_name=last_name,
            first_name=first_name,
            login=login,
            email=email,
            password=password,
        )

        try:
            async with session() as db:
                db.add(user)
                await db.commit()

            return user
        except Exception as e:
            await db.rollback()
            if isinstance(e, IntegrityError):
                # SQLITE_CONSTRAINT_UNIQUE ERROR
                if e.orig.sqlite_errorcode == 2067:
                    return OperationStatus(
                        status="error",
                        message="Пользователь с таким логином уже создан",
                    )

            return OperationStatus(
                status="error", message=f"Ошибка при создании пользователя: {e}"
            )

    async def get_user(
        self, user_id: Optional[int] = None, user_login: Optional[str] = None
    ) -> Optional[User]:
        session = self._get_async_session()

        async with session() as db:
            if user_id:
                user = await db.execute(select(User).where(User.id == user_id))
            elif user_login:
                user = await db.execute(select(User).where(User.login == user_login))

            return user.scalars().one_or_none()

    async def delete_user(self, user_id: int) -> OperationStatus:
        session = self._get_async_session()

        async with session() as db:
            result = await db.execute(delete(User).where(User.id == user_id))

            await db.commit()

            if result.rowcount > 0:
                return OperationStatus(
                    status="success", message="User deleted successfully"
                )
            else:
                return OperationStatus(status="error", message="User not found")

    async def update_user(self, user_id: int, **kwargs) -> OperationStatus:
        session = self._get_async_session()

        async with session() as db:
            user = await db.execute(select(User).where(User.id == user_id))

            user = user.scalars().one_or_none()

            if user is None:
                return OperationStatus(status="error", message="User not found")

            for key, value in kwargs.items():
                if value:
                    setattr(user, key, value)

            await db.commit()

            return OperationStatus(
                status="success", message="User updated successfully"
            )


user_service = UserService()
