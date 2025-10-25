from redis import Redis
from rq import Queue


def get_redis_connection():
    return Redis(host="redis", port=6379)


def get_queue():
    return Queue(connection=get_redis_connection())
