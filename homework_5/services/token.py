from http import HTTPStatus
from typing import Any, Dict

import jwt
from fastapi import Cookie, HTTPException


class TokenService:
    jwt_secret = "my_secret"  # В реальном приложении должен быть в переменных окружения
    jwt_alg = "HS256"

    def create_token(self, data: Dict[str, Any]):
        token = jwt.encode(data, key=self.jwt_secret, algorithm=self.jwt_alg)

        return token

    def verify_token(self, token: str):
        decode_data = jwt.decode(token, key=self.jwt_secret, algorithms=[self.jwt_alg])

        return decode_data

    async def get_auth_cookie(self, access_token: str = Cookie(None)):
        if not access_token or not token_service.verify_token(access_token):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Пользователь неавторизован"
            )


token_service = TokenService()
