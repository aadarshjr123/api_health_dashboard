# Day 28 – API Health Dashboard Setup
- Initialized multi-service Docker stack (API + Redis + Prometheus + Grafana)
- Wrote project diagram and README base


# Day 29 – Health Endpoint + Metrics Integration
- Implemented /health
- Exposed /metrics for Prometheus
- Connected Grafana, created "Requests/sec" panel
- Learned how real services report health and performance


# Day 30 – Grafana Dashboard + Fault Simulation
- Added latency histogram to FastAPI middleware
- Designed multi-panel Grafana dashboard
- Simulated load & rate-limit traffic
- Observed real-time metric shifts in Grafana
- Captured dashboard for portfolio README


# Day 31 – Alerts + Fault Simulation
- Added Prometheus alert rules for latency, rate-limit, and downtime
- Integrated Grafana alert system
- Simulated real failures and observed metric spikes
- Learned how to design alert thresholds for production reliability

# Day 32 – Automatic Recovery & Reliability

✅ Implemented retry decorator with exponential backoff  
✅ Redis RQ auto-rescheduling of failed jobs  
✅ Prometheus metrics for retries and recoveries  
✅ Grafana panels for system resilience tracking  

Key patterns:
- Retry with exponential backoff
- Job requeue on transient failure
- Circuit breaker for repeated API errors (future)
- Health-based auto recovery


# Day 33 – Circuit Breaker & Graceful Degradation
- Added circuit breaker with 3 states and Prometheus metrics  
- Implemented fallback response to avoid user errors  
- Visualized breaker state changes in Grafana  
- Learned how to prevent cascading failures gracefully

# Day 34 – Performance Profiling + Backend Optimization
- Integrated **py-spy** profiler inside Docker to analyze FastAPI performance  
- Fixed permission issues by adding `SYS_PTRACE` + `apparmor:unconfined` in Docker  
- Built a **local py-spy image** to bypass registry access errors  
- Generated **flamegraph (profile.svg)** to visualize CPU usage  
- Identified that most CPU time is in FastAPI routing and event loop (normal behavior)  
- Disabled `--reload` for accurate runtime profiling results  
- Learned how to interpret flamegraphs for spotting bottlenecks  

✅ Key Takeaways:  
- Profiling reveals where the app *actually* spends CPU time  
- Docker needs special privileges for low-level profilers  
- Flamegraphs are essential tools for backend performance tuning  


# Day 35 – Database Optimization & Profiling
✅ Learned indexes and EXPLAIN ANALYZE profiling
✅ Cached expensive queries in Redis
✅ Visualized DB latency in Grafana
✅ Reduced query time by >90%