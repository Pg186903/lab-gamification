from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user
from app.utils.supabase_client import supabase_client

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/bootstrap")
def bootstrap_user(current_user: dict = Depends(get_current_user)):
    user_id = current_user["sub"]

    supabase_client.table("users").upsert(
        {"user_id": user_id}
    ).execute()

    return {"status": "ok"}
