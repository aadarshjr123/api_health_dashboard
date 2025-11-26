# app/caching/read_through.py
import json
from .redis_client import redis
from .metrics import cache_hits, cache_misses
from . import fake_db


async def read_through_user(user_id: int):
    key = f"user:{user_id}"
    cached = await redis.get(key)

    if cached:
        cache_hits.inc()
        return json.loads(cached)

    cache_misses.inc()
    user = await fake_db.get_user(user_id)

    if user is not None:
        await redis.set(key, json.dumps(user), ex=300)  # 5 min TTL

    return user
