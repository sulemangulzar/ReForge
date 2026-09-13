from app.config import settings
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_token(
    data: dict[str, Any]
) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(settings.access_token_expire_minutes)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token: str, secret_key: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.InvalidTokenError as exc:
        raise ValueError("Invalid token") from exc
