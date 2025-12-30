from jose import jwt, JWTError
from fastapi import HTTPException, status
from os import getenv

JWT_SECRET = getenv("SUPABASE_JWT_SECRET")
JWT_ALGORITHM = "HS256"


def verify_jwt_token(token: str) -> dict:
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
