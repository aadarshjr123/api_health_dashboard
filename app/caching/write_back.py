# app/caching/write_back.py
import json
from .redis_client import redis
from .metrics import writeback_queue_size
from . import fake_db  # for immediate cache write


WRITEBACK_QUEUE_KEY = "writeback_queue"


async def write_back_user(payload: dict):
    """
    1) Write to cache immediately
    2) Push update into write-back queue for DB worker
    """
    user_id = payload["id"]

    # Update cache now
    updated = await fake_db.update_user(user_id, payload)
    await redis.set(f"user:{user_id}", json.dumps(updated), ex=300)

    # Push to queue for background DB sync (Day 43 worker)
    await redis.lpush(WRITEBACK_QUEUE_KEY, json.dumps(payload))

    # Track queue size
    queue_len = await redis.llen(WRITEBACK_QUEUE_KEY)
    writeback_queue_size.set(queue_len)

    return updated
