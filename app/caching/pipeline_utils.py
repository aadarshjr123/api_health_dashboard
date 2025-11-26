# app/caching/pipeline_utils.py
from typing import List, Dict, Any
import json
from .redis_client import redis


async def get_many_users_from_cache(user_ids: List[int]) -> Dict[int, Any]:
    """
    Use Redis pipelining to fetch multiple users in one round-trip.
    Returns a dict: { user_id: user_data_or_None }
    """
    pipe = redis.pipeline()
    keys = [f"user:{uid}" for uid in user_ids]

    for key in keys:
        pipe.get(key)

    raw_results = await pipe.execute()

    result: Dict[int, Any] = {}
    for uid, raw in zip(user_ids, raw_results):
        result[uid] = json.loads(raw) if raw else None

    return result
