import redis.asyncio as redis
from typing import AsyncGenerator
from redis.asyncio import Redis  # <-- Import Redis class here

REDIS_URL = "redis://localhost:6379"

redis_client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_redis() -> AsyncGenerator[Redis, None]:
    try:
        yield redis_client
    finally:
        await redis_client.close()
