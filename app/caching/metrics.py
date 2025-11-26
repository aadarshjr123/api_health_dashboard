# app/caching/metrics.py
from prometheus_client import Counter, Gauge

# Total cache hits and misses
cache_hits = Counter("cache_hits_total", "Total cache hits")
cache_misses = Counter("cache_misses_total", "Total cache misses")

# Size of the write-back queue
writeback_queue_size = Gauge(
    "writeback_queue_size",
    "Size of writeback queue in Redis"
)
