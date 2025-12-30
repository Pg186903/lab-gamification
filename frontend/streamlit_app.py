"""
Main Streamlit entrypoint for the Gamified Stomata Labs POC frontend.

Applies global neon theme, validates Supabase auth token, and routes pages.
"""

from __future__ import annotations

import streamlit as st

from utils.api_client import fetch_current_user

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Stomata Labs – Gamified Ops",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Neon Theme CSS
# ---------------------------------------------------------
NEON_CSS = """
<style>
html, body, [class*="css"]  {
    background-color: #0b0f14;
    color: #e5e7eb;
}

.block-container {
    padding-top: 1.5rem;
}

.sidebar .sidebar-content {
    background-color: #0b0f14;
}

.neon-card {
    background: #121826;
    border-radius: 16px;
    padding: 1.2rem;
    box-shadow: 0 0 10px rgba(0,255,156,0.15);
    transition: all 0.2s ease-in-out;
}

.neon-card:hover {
    box-shadow: 0 0 18px rgba(139,92,246,0.35);
    transform: translateY(-2px);
}

.neon-title {
    color: #00ff9c;
    font-weight: 600;
}

.neon-subtitle {
    color: #8b5cf6;
}

button[kind="primary"] {
    background: linear-gradient(90deg, #00ff9c, #8b5cf6);
    color: #0b0f14;
    border-radius: 12px;
}
</style>
"""

st.markdown(NEON_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Authentication State
# ---------------------------------------------------------
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if not st.session_state.access_token:
    st.switch_page("pages/auth.py")


def render_login() -> None:
    """Simple token-based login screen."""
    st.title("🔐 Stomata Labs Ops Portal")

    with st.container():
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        token = st.text_input(
            "Supabase Access Token",
            type="password",
            help="Paste your Supabase access token here.",
        )
        if st.button("Login"):
            user = fetch_current_user(token)
            if user:
                st.session_state.access_token = token
                st.session_state.current_user = user
                st.rerun()
            else:
                st.error("Invalid token.")
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Main Layout
# ---------------------------------------------------------
if not st.session_state.access_token:
    render_login()
    st.stop()

user = st.session_state.current_user

with st.sidebar:
    st.markdown("## 🌿 Stomata Labs")
    st.caption(f"Logged in as **{user.get('email', 'Unknown')}**")

    page = st.radio(
        "Navigate",
        ["Dashboard", "Leaderboard", "Analytics", "Quizzes"],
        label_visibility="collapsed",
    )

    if st.button("Logout"):
        st.session_state.access_token = None
        st.session_state.current_user = None
        st.rerun()

# ---------------------------------------------------------
# Page Routing
# ---------------------------------------------------------
if page == "Dashboard":
    st.switch_page("pages/dashboard.py")
elif page == "Leaderboard":
    st.switch_page("pages/leaderboard.py")
elif page == "Analytics":
    st.switch_page("pages/analytics.py")
elif page == "Quizzes":
    st.switch_page("pages/quizzes.py")
