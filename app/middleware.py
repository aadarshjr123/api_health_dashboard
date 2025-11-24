import time
from datetime import datetime
from fastapi import Request
from app.metrics import METRICS
from app.db import engine
from app.config import redis_client
import logging, json, time

json_logger = logging.getLogger("app.json")
json_logger.setLevel(logging.INFO)
json_logger.addHandler(logging.StreamHandler())


async def json_logger_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 3)

    log = {
        "req_id": getattr(request.state, "correlation_id", None),
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration": duration,
        "ip": request.client.host,
    }

    json_logger.info(json.dumps(log))
    return response


async def track_active_users(request: Request, call_next):
    username = request.headers.get("user")
    if username:
        redis_client.hset("active_users", username, datetime.utcnow().isoformat())
    response = await call_next(request)
    return response


async def prometheus_middleware(request: Request, call_next):
    """Tracks request count and latency."""
    start_time = time.time()
    METRICS["requests_total"].inc()
    response = await call_next(request)
    METRICS["request_latency"].observe(time.time() - start_time)
    return response


async def count_ip_requests(request: Request, call_next):
    ip = request.client.host
    METRICS["ip_request_counter"].labels(ip=ip).inc()
    return await call_next(request)


async def track_db_pool(request, call_next):
    """
    Update Prometheus metric for DB pool usage on every request.
    """
    try:
        sync_pool = engine.sync_engine.pool  # async engine uses a sync pool underneath
        active_conns = sync_pool.checkedout()
        METRICS["db_pool_in_use"].set(active_conns)
    except Exception as e:
        # optional: log errors if pool is not initialized yet
        print(f"[WARN] Could not measure DB pool usage: {e}")

    response = await call_next(request)
    return response
