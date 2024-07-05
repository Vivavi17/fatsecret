import redis.asyncio as redis
from config import REDIS_HOST, REDIS_PORT

cache = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True")
