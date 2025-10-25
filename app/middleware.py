import time
from fastapi import Request
from app.metrics import METRICS


async def prometheus_middleware(request: Request, call_next):
    """Tracks request count and latency."""
    start_time = time.time()
    METRICS["requests_total"].inc()
    response = await call_next(request)
    METRICS["request_latency"].observe(time.time() - start_time)
    return response
