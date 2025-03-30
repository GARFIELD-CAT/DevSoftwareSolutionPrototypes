from typing import Optional

from redis.asyncio import Redis

COMPONENT_NAME = "cache_storage"


class CacheStorage:
    def __init__(self, host: str, port: int):
        self.redis = Redis(host=host, port=port)

    async def set(self, key: str, value: str, expire_time: int = 60) -> None:
        await self.redis.set(self._redis_key(key), value, ex=expire_time)

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(self._redis_key(key))

    async def delete(self, key: str) -> None:
        return await self.redis.delete(self._redis_key(key))

    @staticmethod
    def _redis_key(key):
        return f"{COMPONENT_NAME}:{key}"


cache_storage = CacheStorage(host="localhost", port=6379)
