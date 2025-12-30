from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/")
def log_event(
    data: dict,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["sub"]

    return {
        "message": "Event logged",
        "user_id": user_id,
    }
