"""Password and JWT helpers. Raw passwords and raw refresh tokens are never persisted."""

from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Literal
from uuid import uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import get_settings

password_hasher = PasswordHasher()
TokenKind = Literal["access", "refresh"]


class TokenValidationError(Exception):
    """Raised when a token is missing, malformed, expired, or the wrong kind."""


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def hash_refresh_token(token: str) -> str:
    """Use a one-way digest so database exposure does not expose usable JWTs."""
    return sha256(token.encode("utf-8")).hexdigest()


def create_token(subject: str, token_type: TokenKind, expires_delta: timedelta) -> tuple[str, str, datetime]:
    settings = get_settings()
    token_id = str(uuid4())
    expires_at = datetime.now(UTC) + expires_delta
    payload = {"sub": subject, "jti": token_id, "type": token_type, "iat": datetime.now(UTC), "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256"), token_id, expires_at


def create_access_token(user_id: str, expires_delta: timedelta | None = None) -> tuple[str, str, datetime]:
    settings = get_settings()
    return create_token(user_id, "access", expires_delta or timedelta(minutes=settings.access_token_expire_minutes))


def create_refresh_token(user_id: str) -> tuple[str, str, datetime]:
    settings = get_settings()
    return create_token(user_id, "refresh", timedelta(days=settings.refresh_token_expire_days))


def decode_token(token: str, expected_type: TokenKind) -> dict[str, str]:
    try:
        payload = jwt.decode(token, get_settings().jwt_secret, algorithms=["HS256"])
    except ExpiredSignatureError as exc:
        raise TokenValidationError("Token has expired") from exc
    except InvalidTokenError as exc:
        raise TokenValidationError("Token is invalid") from exc
    if payload.get("type") != expected_type or not payload.get("sub") or not payload.get("jti"):
        raise TokenValidationError("Token is invalid")
    return {"sub": str(payload["sub"]), "jti": str(payload["jti"])}
