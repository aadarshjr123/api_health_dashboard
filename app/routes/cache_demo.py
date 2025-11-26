from fastapi import APIRouter, HTTPException,Query
from typing import List
import json, time
from app.config import redis_client

# NEW IMPORTS FOR ADVANCED CACHING
from app.caching.read_through import read_through_user
from app.caching.write_through import write_through_user
from app.caching.write_back import write_back_user
from app.caching.pipeline_utils import get_many_users_from_cache

router = APIRouter()


# ---------------------------------------------------------
# ORIGINAL CODE (unchanged)
# ---------------------------------------------------------

@router.get("/heavy")
def heavy_calc():
    """Simulate a CPU-heavy computation with Redis caching."""
    key = "heavy_result"

    if cached := redis_client.get(key):
        return json.loads(cached) | {"cached": True}

    # Simulate expensive work
    time.sleep(3)
    result = {"data": "complex calc result", "cached": False}
    redis_client.setex(key, 60, json.dumps(result))  # cache for 60 seconds
    return result


@router.delete("/cache")
def clear_cache():
    """Clear all Redis cache entries."""
    redis_client.flushall()
    return {"msg": "Cache cleared ✅"}


# ---------------------------------------------------------
# NEW — REDIS PIPELINING DEMO
# ---------------------------------------------------------

@router.get("/users/batch")
async def batch_read_from_cache(ids: List[int] = Query(...)):
    """
    Example: GET /users/batch?ids=1&ids=2&ids=3
    """
    data = await get_many_users_from_cache(ids)
    return {"ids": ids, "data": data}


# ---------------------------------------------------------
# NEW — READ-THROUGH CACHE DEMO
# ---------------------------------------------------------

@router.get("/users/{user_id}")
async def get_user_read_through(user_id: int):
    """
    First call = slow DB
    Later calls = Redis (fast)
    """
    user = await read_through_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"mode": "read-through", "user": user}


# ---------------------------------------------------------
# NEW — WRITE-THROUGH CACHE DEMO
# ---------------------------------------------------------

@router.put("/users/{user_id}")
async def update_user_write_through(user_id: int, payload: dict):
    """
    Updates DB and Redis instantly.
    """
    updated = await write_through_user(user_id, payload)
    return {"mode": "write-through", "user": updated}


# ---------------------------------------------------------
# NEW — WRITE-BACK CACHE DEMO
# ---------------------------------------------------------

@router.post("/users/write-back")
async def update_user_write_back(payload: dict):
    """
    Writes to Redis now,
    queues DB update for later (worker on Day 43).
    """
    updated = await write_back_user(payload)
    return {"mode": "write-back", "user": updated}



