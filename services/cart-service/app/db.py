# app/db.py
import aioredis
from typing import AsyncGenerator
from fastapi import Depends

# Redis connection URL, typically read from env (for now hardcoded example)
REDIS_URL = "redis://localhost:6379"

# Create Redis client instance, but connection is lazy (not connected yet)
redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """
    FastAPI dependency that provides a Redis client instance for request handlers.
    Ensures proper connection lifecycle management.
    """
    try:
        yield redis
    finally:
        # Connection cleanup (optional for aioredis, but good practice)
        await redis.close()
        await redis.wait_closed()
