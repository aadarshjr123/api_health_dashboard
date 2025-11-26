# app/caching/fake_db.py
import asyncio

# Pretend this is a slow database
_FAKE_DB = {
    1: {"id": 1, "name": "Luca", "role": "dog"},
    2: {"id": 2, "name": "Aadarsh", "role": "human"},
}

async def get_user(user_id: int):
    # simulate slow DB
    await asyncio.sleep(0.5)
    return _FAKE_DB.get(user_id)

async def update_user(user_id: int, payload: dict):
    await asyncio.sleep(0.5)
    if user_id not in _FAKE_DB:
        _FAKE_DB[user_id] = {"id": user_id}
    _FAKE_DB[user_id].update(payload)
    return _FAKE_DB[user_id]
