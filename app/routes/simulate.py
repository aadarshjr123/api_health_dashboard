from fastapi import APIRouter, HTTPException
import random, time
from app.utils.retry import retry
from app.metrics import METRICS

router = APIRouter()


# --- Retry Simulation ---
@retry(max_retries=3, delay=1, backoff=2)
def resilient_task():
    if random.random() < 0.7:
        METRICS["retry_attempts_total"].inc()
        raise Exception("Simulated transient failure")
    METRICS["retry_success_total"].inc()
    return {"status": "ok"}


@router.get("/resilient-task")
def resilient_task_route():
    """Simulate a retried task and expose resilience metrics."""
    return resilient_task()


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


@router.get("/limited")
def limited():
    METRICS["rate_limited_total"].inc()
    raise HTTPException(status_code=429, detail="Too many requests 🚫")
