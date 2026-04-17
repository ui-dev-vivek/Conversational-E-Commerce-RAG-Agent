from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=15)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)