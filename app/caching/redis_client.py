# app/caching/redis_client.py
import os
from redis.asyncio import Redis

# Use same Redis instance as your RQ / docker-compose (likely host "redis", port 6379)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
