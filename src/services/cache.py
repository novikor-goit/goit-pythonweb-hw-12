import redis.asyncio as redis
from redis.asyncio.client import Redis

from src.conf.config import settings


class Cache:
    _redis_client: Redis | None = None

    @classmethod
    def client(cls) -> Redis:
        if cls._redis_client is None:
            cls._redis_client = redis.Redis(
                host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
            )
        return cls._redis_client
