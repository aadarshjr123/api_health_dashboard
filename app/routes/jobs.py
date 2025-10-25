from fastapi import APIRouter
from rq import Retry
from app.config import get_queue
from app.workers.tasks import heavy_computation, process_image
from app.metrics import METRICS

router = APIRouter()
queue = get_queue()


@router.get("/process-job/{n}")
def process_job(n: int):
    """Queue a heavy computation job."""
    job = queue.enqueue(heavy_computation, n)
    return {"job_id": job.id, "status": "queued"}


@router.get("/retry-job")
def retry_job():
    """Queue a job that may fail and will auto-retry."""
    job = queue.enqueue(
        process_image, "test.png", retry=Retry(max=3, interval=[10, 20, 40])
    )
    return {"job_id": job.id, "status": "queued with retry"}
