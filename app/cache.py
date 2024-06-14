import redis.asyncio as redis

from app.config import settings

cache = redis.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}?decode_responses=True"
)
