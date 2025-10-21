from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Optional, Dict
import uuid

from app.core.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    truncated = password[:72]
    return pwd_ctx.hash(truncated)

def verify_password(plain_password: str, password: str) -> bool:
    return pwd_ctx.verify(plain_password[:72], password)

def create_access_token(subject: str) -> tuple[str, datetime]:
    expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": str(subject), "type": "access", "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token, expire

def create_refresh_token() -> tuple[str, datetime]:
    token = str(uuid.uuid4())
    expire = datetime.utcnow() + timedelta(days=int(settings.REFRESH_TOKEN_EXPIRE_DAYS))
    return token, expire

def decode_token(token: str) -> Optional[Dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
