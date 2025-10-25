import time, random
from rq import Retry
from app.metrics import METRICS
import requests


def heavy_computation(n):
    """Run a long job and notify API when done."""
    time.sleep(3)
    # Notify FastAPI that job finished
    try:
        requests.post("http://api:8000/internal/job-finished")
    except Exception as e:
        print("⚠️ Failed to notify API:", e)
    return {"status": f"Job {n} done"}


def process_image(file: str):
    """
    Simulate a job that sometimes fails.
    Redis RQ will retry automatically with exponential backoff.
    """
    if random.random() < 0.5:
        raise Exception("Temporary failure while processing image")
    METRICS["job_finished_total"].inc()
    return f"✅ Processed: {file}"
