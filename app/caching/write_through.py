# app/caching/write_through.py
import json
from .redis_client import redis
from . import fake_db


async def write_through_user(user_id: int, payload: dict):
    # 1) Update "DB"
    updated = await fake_db.update_user(user_id, payload)

    # 2) Update cache so it stays in sync
    await redis.set(f"user:{user_id}", json.dumps(updated), ex=300)

    return updated
