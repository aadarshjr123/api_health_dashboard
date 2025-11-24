from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth import (
    create_token,
    verify_refresh_token,
    decode_token,
    hash_password,
    verify_password,
    create_refresh_token,
)
from app.metrics import METRICS
from app.config import redis_client

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Fake DB for demo (you can later replace with Postgres)
users_db = {"aadarsh": hash_password("test123")}


@router.post("/login")
async def login(username: str, password: str):
    METRICS["auth_requests_total"].inc()

    if username not in users_db or not verify_password(password, users_db[username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_token({"sub": username})
    refresh = create_refresh_token(username)

    return {"access_token": access, "refresh_token": refresh}


@router.get("/active-users")
async def active_users():
    return redis_client.hgetall("active_users")


@router.post("/refresh")
async def refresh(username: str, refresh_token: str):
    if not verify_refresh_token(username, refresh_token):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_token({"sub": username})
    return {"access_token": new_access}


@router.get("/secure")
async def secure_route(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"msg": f"Welcome {payload['sub']}!"}
