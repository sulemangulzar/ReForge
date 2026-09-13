from app.config import settings
from datetime import datetime, timedelta, timezone
from hashlib import sha256
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
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def hash_token(token: str) -> str:
    return sha256(token.encode()).hexdigest()


def create_refresh_token(data: dict[str, Any]) -> str:
    payload = data.copy()
    payload["type"] = "refresh"
    payload["exp"] = datetime.now(timezone.utc) + timedelta(days=7)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token: str, secret_key: str | None = None) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            secret_key or settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except jwt.InvalidTokenError as exc:
        raise ValueError("Invalid token") from exc


def verify_refresh_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")
        return payload
    except (jwt.InvalidTokenError, KeyError, TypeError) as exc:
        raise ValueError("Invalid refresh token") from exc


def create_password_reset_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.email_confirmation_hours)
    payload = {"sub": email, "purpose": "password_reset", "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_password_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("purpose") != "password_reset":
            raise ValueError("Invalid reset token")
        return payload["sub"]
    except (jwt.InvalidTokenError, KeyError, TypeError) as exc:
        raise ValueError("Invalid reset token") from exc


def create_email_confirmation_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.email_confirmation_hours)
    payload = {"sub": email, "purpose": "email_confirmation", "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def verify_email_confirmation_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("purpose") != "email_confirmation":
            raise ValueError("Invalid confirmation token")
        return payload["sub"]
    except (jwt.InvalidTokenError, KeyError, TypeError) as exc:
        raise ValueError("Invalid confirmation token") from exc
