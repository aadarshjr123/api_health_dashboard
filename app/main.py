from fastapi import FastAPI, Request, HTTPException
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, Histogram
from fastapi.responses import PlainTextResponse
from datetime import datetime
import time

app = FastAPI()
start_time = datetime.now()

http_requests_total = Counter("http_requests_total", "Total HTTP requests")
rate_limited_total = Counter("rate_limited_total", "Rate-limited requests")

request_latency = Histogram(
    "http_request_duration_seconds", "Latency of HTTP requests in seconds"
)


@app.middleware("http")
async def count_requests(request: Request, call_next):
    start = time.time()
    http_requests_total.inc()
    response = await call_next(request)
    duration = time.time() - start
    request_latency.observe(duration)
    return response


@app.get("/")
def root():
    return {"message": "API Health Dashboard running 🚀"}


@app.get("/health")
def health():
    uptime = (datetime.now() - start_time).seconds
    return {
        "status": "ok",
        "uptime_seconds": uptime,
        "requests_total": http_requests_total._value.get(),
        "rate_limited_total": rate_limited_total._value.get(),
    }


@app.get("/limited")
def limited():
    # Simulate a user hitting a rate limit
    rate_limited_total.inc()
    raise HTTPException(status_code=429, detail="Too many requests 🚫")


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
