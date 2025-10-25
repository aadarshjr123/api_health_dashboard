from prometheus_client import Counter, Histogram

http_requests_total = Counter("http_requests_total", "Total HTTP requests")
rate_limited_total = Counter("rate_limited_total", "Rate-limited requests")
job_finished_total = Counter("job_finished_total", "Completed background jobs")

# 🔥 New Resilience Metrics
retry_attempts_total = Counter("retry_attempts_total", "Total retry attempts")
retry_success_total = Counter("retry_success_total", "Successful retries after failure")

request_latency = Histogram(
    "http_request_duration_seconds", "Latency of HTTP requests in seconds"
)

METRICS = {
    "requests_total": http_requests_total,
    "rate_limited_total": rate_limited_total,
    "job_finished_total": job_finished_total,
    "retry_attempts_total": retry_attempts_total,
    "retry_success_total": retry_success_total,
    "request_latency": request_latency,
}
