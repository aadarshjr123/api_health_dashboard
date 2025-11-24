from fastapi import APIRouter
import json, time
from app.config import redis_client

router = APIRouter()


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
