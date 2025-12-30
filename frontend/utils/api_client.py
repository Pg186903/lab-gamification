from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

API_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")


def _get_supabase_client():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError("SUPABASE_URL or SUPABASE_ANON_KEY not set in .env")

    return create_client(supabase_url, supabase_key)


def _auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# ---------------------------------------------------------
# Supabase Auth APIs
# ---------------------------------------------------------
def signup_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    supabase = _get_supabase_client()
    response = supabase.auth.sign_up(
        {"email": payload["email"], "password": payload["password"]}
    )

    if response.user is None:
        raise ValueError("Signup failed")

    return {"full_name": payload["full_name"], "email": payload["email"]}


def login_user(email: str, password: str) -> Optional[str]:
    supabase = _get_supabase_client()
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        return response.session.access_token
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------
# FastAPI Backend APIs
# ---------------------------------------------------------
def fetch_current_user(token: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(
            f"{API_BASE_URL}/users/me",
            headers=_auth_headers(token),
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error("Failed to authenticate user.")
        st.exception(exc)
        return None


def bootstrap_user(token: str) -> bool:
    try:
        response = requests.post(
            f"{API_BASE_URL}/users/bootstrap",
            headers=_auth_headers(token),
            timeout=10,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        st.error("Bootstrap failed.")
        st.exception(exc)
        return False


def log_event(token: str, feature: str, action: str, metadata: dict | None = None) -> bool:
    payload = {"feature": feature, "action": action, "metadata": metadata or {}}

    try:
        response = requests.post(
            f"{API_BASE_URL}/events",
            json=payload,
            headers=_auth_headers(token),
            timeout=10,
        )
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        st.warning("Could not log event.")
        st.exception(exc)
        return False
