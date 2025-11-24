from prometheus_client import Counter, Histogram, Gauge

http_requests_total = Counter("http_requests_total", "Total HTTP requests")
rate_limited_total = Counter("rate_limited_total", "Rate-limited requests")
job_finished_total = Counter("job_finished_total", "Completed background jobs")

# 🔥 New Resilience Metrics
retry_attempts_total = Counter("retry_attempts_total", "Total retry attempts")
retry_success_total = Counter("retry_success_total", "Successful retries after failure")

ip_request_counter = Counter(
    "api_requests_total", "Total number of API requests per IP", ["ip"]
)

request_latency = Histogram(
    "request_latency_seconds",
    "Latency per endpoint (seconds)",
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2, 5],
)


circuit_breaker_state = Gauge(
    "circuit_breaker_state",
    "Current state of circuit breaker (0=closed,1=open,2=half-open)",
)

db_pool_in_use = Gauge("db_pool_in_use_connections", "Active connections in pool")
db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Duration of database queries in seconds",
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5],
)

auth_requests_total = Counter(
    "auth_requests_total", "Total number of authentication login attempts"
)

METRICS = {
    "requests_total": http_requests_total,
    "rate_limited_total": rate_limited_total,
    "job_finished_total": job_finished_total,
    "retry_attempts_total": retry_attempts_total,
    "retry_success_total": retry_success_total,
    "request_latency": request_latency,
    "circuit_breaker_state": circuit_breaker_state,
    "db_pool_in_use": db_pool_in_use,
    "db_query_duration_seconds": db_query_duration_seconds,
    "ip_request_counter": ip_request_counter,
    "auth_requests_total": auth_requests_total,
}
