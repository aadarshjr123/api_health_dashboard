from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import redis_client

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(pw: str):
    return pwd_context.hash(pw)


def verify_password(pw: str, hashed: str):
    return pwd_context.verify(pw, hashed)


def create_token(data: dict, minutes: int = 30):
    data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(username: str):
    token = create_token({"sub": username}, minutes=60 * 24 * 7)  # 7 days
    redis_client.setex(f"refresh:{username}", 60 * 60 * 24 * 7, token)
    return token


def verify_refresh_token(username: str, token: str):
    stored = redis_client.get(f"refresh:{username}")
    return stored == token


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
