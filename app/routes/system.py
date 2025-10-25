from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from datetime import datetime
from app.metrics import METRICS

router = APIRouter()
start_time = datetime.now()


@router.get("/")
def root():
    return {"message": "API Health Dashboard running 🚀"}


@router.get("/health")
def health():
    uptime = (datetime.now() - start_time).seconds
    return {
        "status": "ok",
        "uptime_seconds": uptime,
        "requests_total": METRICS["requests_total"]._value.get(),
        "rate_limited_total": METRICS["rate_limited_total"]._value.get(),
        "job_finished_total": METRICS["job_finished_total"]._value.get(),
    }


@router.post("/internal/job-finished", status_code=status.HTTP_204_NO_CONTENT)
def job_finished():
    """Internal endpoint for worker job completion tracking."""
    METRICS["job_finished_total"].inc()


@router.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
