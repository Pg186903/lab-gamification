from fastapi import Header, HTTPException, status
from typing import Annotated
from app.utils.auth import verify_jwt_token


def get_current_user(
    authorization: Annotated[str, Header(...)],
) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header",
        )

    token = authorization.removeprefix("Bearer ").strip()
    return verify_jwt_token(token)
