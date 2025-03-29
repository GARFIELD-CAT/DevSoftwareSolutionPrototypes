from passlib.hash import pbkdf2_sha256


class PasswordService:
    _salt = "my_salt"  # В реальном приложении должен быть в переменных окружения

    def create_hashed_password(self, password: str) -> str:
        return pbkdf2_sha256.hash(password + self._salt)

    def verify_password(self, password: str, hash: str) -> bool:
        return pbkdf2_sha256.verify(password + self._salt, hash)


password_service = PasswordService()
