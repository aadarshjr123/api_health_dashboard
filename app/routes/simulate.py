from fastapi import APIRouter, HTTPException, Request
import random, time
from app.utils.retry import retry
from app.utils.circuit_breaker import CircuitBreaker
from app.metrics import METRICS

router = APIRouter()
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=15)


# 🧩 Cached fallback response for graceful degradation
cached_response = {"message": "⚠️ Temporary data unavailable. Showing cached summary."}


# --- Retry Simulation ---
@breaker
@retry(max_retries=3, delay=1, backoff=2)
def resilient_task():
    if random.random() < 0.7:
        METRICS["retry_attempts_total"].inc()
        raise Exception("Simulated transient failure")
    METRICS["retry_success_total"].inc()
    return {"status": "✅ Live response from stable service"}


@router.get("/resilient-task")
def resilient_task_route():
    """Simulate a retried task and gracefully degrade when circuit is OPEN."""
    try:
        return resilient_task()
    except Exception as e:
        # If the circuit is OPEN → return cached or simplified data
        if breaker.state == "OPEN":
            return cached_response
        # Otherwise, return a clear transient failure message (optional)
        return {"error": str(e), "circuit_state": breaker.state}


# --- Existing Simulation Endpoints ---
@retry(max_retries=3, delay=1, backoff=2)
def call_external_service():
    if random.random() < 0.6:
        raise Exception("API call failed")
    return {"result": "success"}


@router.get("/retry-demo")
def retry_demo():
    return call_external_service()


@router.get("/slow")
def slow_endpoint():
    time.sleep(2)
    return {"message": "Simulated delay done!"}


@router.get("/limited/data")
async def limited_data(request: Request):
    # Access limiter from FastAPI shared state
    limiter = request.app.state.limiter

    # Apply rate limit (10 requests per minute per IP)
    @limiter.limit("10/minute")
    async def _inner(request: Request):
        return {"message": "You are under rate limit!"}

    return await _inner(request)


@router.get("/limited")
def limited():
    METRICS["rate_limited_total"].inc()
    raise HTTPException(status_code=429, detail="Too many requests 🚫")
