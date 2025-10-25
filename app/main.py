from fastapi import FastAPI
from app.middleware import prometheus_middleware
from app.routes import jobs, simulate, system


def create_app():
    app = FastAPI(title="API Health Dashboard", version="1.0.0")

    # Add middleware
    app.middleware("http")(prometheus_middleware)

    # Register route modules
    app.include_router(system.router)
    app.include_router(jobs.router)
    app.include_router(simulate.router)

    return app


app = create_app()
