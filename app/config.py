import psycopg2, time
from redis import Redis
from rq import Queue


def get_redis_connection():
    return Redis(host="redis", port=6379, decode_responses=True)


def get_queue():
    return Queue(connection=get_redis_connection())


def get_postgres_connection(retries=10, delay=2):
    for attempt in range(1, retries + 1):
        try:
            return psycopg2.connect(
                host="db", port=5432, user="admin", password="admin", dbname="appdb"
            )
        except psycopg2.OperationalError as e:
            print(f"⚠️ Attempt {attempt}: Database not ready ({e})")
            time.sleep(delay)
    raise Exception("❌ Could not connect to Postgres after multiple retries.")


# global connections
redis_client = get_redis_connection()
postgres_conn = get_postgres_connection()
