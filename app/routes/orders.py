from fastapi import APIRouter, Depends
from sqlalchemy import text
from app.config import postgres_conn, redis_client
from prometheus_client import Summary
import json
import time
from app.db import get_db
from app.metrics import METRICS
from opentelemetry import trace

router = APIRouter()
tracer = trace.get_tracer(__name__)


@router.get("/orders")
def list_orders(limit: int = 10):
    with postgres_conn.cursor() as cur:
        cur.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT %s;", (limit,))
        rows = cur.fetchall()
    return {"rows": rows}


@router.get("/orders/cached")
def cached_orders(limit: int = 100):
    key = f"orders:{limit}"
    if cached := redis_client.get(key):
        return json.loads(cached) | {"cached": True}

    with postgres_conn.cursor() as cur:
        cur.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT %s;", (limit,))
        rows = cur.fetchall()

    result = {"rows": rows, "cached": False}
    redis_client.setex(key, 60, json.dumps(result, default=str))  # TTL = 60 seconds
    return result


@router.get("/orders/profiled")
def profiled_orders():
    start = time.perf_counter()
    try:
        with postgres_conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM orders;")
            count = cur.fetchone()[0]
            return {"count": count}
    finally:
        duration = time.perf_counter() - start
        METRICS["db_query_duration_seconds"].observe(duration)


@router.get("/orders/async")
async def get_orders(limit: int = 100, db=Depends(get_db)):
    with tracer.start_as_current_span("fetch_orders_from_db"):
        start = time.perf_counter()
        try:
            result = await db.execute(
                text("SELECT * FROM orders ORDER BY created_at DESC LIMIT :limit"),
                {"limit": limit},
            )
            rows = result.fetchall()
            return {"count": len(rows), "rows": [dict(r._mapping) for r in rows]}
        finally:
            duration = time.perf_counter() - start
            METRICS["db_query_duration_seconds"].observe(duration)
