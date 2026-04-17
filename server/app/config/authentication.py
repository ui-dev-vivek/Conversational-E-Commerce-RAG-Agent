import hashlib
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "AJ@1120NEW"  # use env in real apps
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def hash_password(password: str) -> str:
    # Step 1: Normalize to fixed length (avoids 72-byte issue)
    normalized = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Step 2: Hash using bcrypt
    return pwd_context.hash(normalized)


def verify_password(password: str, hashed_password: str) -> bool:
    normalized = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.verify(normalized, hashed_password)


def create_access_token(data):
    payload = {
        "sub": data,
        "type": "access",
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: str):
    payload = {
        "sub": data,
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
