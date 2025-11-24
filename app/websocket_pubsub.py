import redis
import asyncio
import json

r = redis.Redis(host="redis", port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe("chat_channel")


async def redis_listener(manager):
    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            await manager.broadcast(data)
