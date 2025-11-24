from fastapi import FastAPI
import asyncio

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.middleware import (
    track_active_users,
    prometheus_middleware,
    track_db_pool,
    count_ip_requests,
    json_logger_middleware,
)

from app.middlewares.correlation import CorrelationIDMiddleware
from app.routes import (
    jobs,
    simulate,
    system,
    cache_demo,
    orders,
    auth_routes,
)

from app.tracing import setup_tracing

setup_tracing()
# OPTIONAL WebSocket Pub/Sub (only if file exists)
try:
    from app.websocket_pubsub import redis_listener, manager

    HAS_PUBSUB = True
except ImportError:
    HAS_PUBSUB = False


def create_app():
    app = FastAPI(title="API Health Dashboard", version="1.0.0")

    # ---- Rate Limiting ----
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ---- Middleware ----
    app.add_middleware(CorrelationIDMiddleware)
    app.middleware("http")(track_active_users)
    app.middleware("http")(count_ip_requests)
    app.middleware("http")(prometheus_middleware)
    app.middleware("http")(track_db_pool)
    app.middleware("http")(json_logger_middleware)

    # ---- Routes ----
    app.include_router(system.router)
    app.include_router(jobs.router)
    app.include_router(simulate.router)
    app.include_router(cache_demo.router)
    app.include_router(orders.router)
    app.include_router(auth_routes.router)

    # ---- Startup Event (Only if Pub/Sub exists) ----
    if HAS_PUBSUB:

        async def start_pubsub():
            asyncio.create_task(redis_listener(manager))

        app.add_event_handler("startup", start_pubsub)

    return app


app = create_app()
