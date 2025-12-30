from __future__ import annotations

from os import getenv

from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

JWT_SECRET = getenv("SUPABASE_JWT_SECRET")
JWT_ALGORITHM = "HS256"


def verify_jwt_token(token: str) -> dict:
    """Verify and decode Supabase JWT."""
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience="authenticated",
        )
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc


def get_current_user(authorization: str = Header(...)) -> dict:
    """
    FastAPI dependency to get the current authenticated user.
    Extracts Bearer token from Authorization header.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header",
        )

    token = authorization.removeprefix("Bearer ").strip()
    return verify_jwt_token(token)
