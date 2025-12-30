from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/bootstrap")
def bootstrap_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """
    Create a user profile row if it does not already exist.
    This links auth.users.id → users.user_id.
    """
    user_id = current_user["sub"]

    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        db.add(User(user_id=user_id))
        db.commit()

    return {"status": "ok"}
