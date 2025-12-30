"""
Leaderboard page for the Stomata Labs gamified frontend.
Shows global rankings with a neon-styled UI.
"""

from __future__ import annotations

import streamlit as st

from utils.api_client import log_event

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.title("🏆 Leaderboard")
st.markdown(
    "<p class='neon-subtitle'>Top performers across locations</p>",
    unsafe_allow_html=True,
)

token = st.session_state.get("access_token")

if not token:
    st.error("You are not authenticated.")
    st.stop()

# Log page visit
log_event(token, feature="leaderboard", action="open")

# ---------------------------------------------------------
# Helper to render a leaderboard row
# ---------------------------------------------------------
def render_row(rank: int, name: str, points: int) -> None:
    """Render a single leaderboard row."""
    st.markdown(
        f"""
        <div class="neon-card" style="display:flex;justify-content:space-between;">
            <div>
                <span class="neon-title">#{rank}</span>
                <span style="margin-left:12px;">{name}</span>
            </div>
            <div style="font-weight:600;color:#00ff9c;">
                {points} pts
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Dummy leaderboard data (replace with API later)
# ---------------------------------------------------------
leaderboard_data = [
    {"name": "Aarav", "points": 1820},
    {"name": "Neha", "points": 1690},
    {"name": "Rohan", "points": 1510},
    {"name": "Priya", "points": 1430},
    {"name": "Kunal", "points": 1320},
]

# ---------------------------------------------------------
# Render leaderboard
# ---------------------------------------------------------
for index, user in enumerate(leaderboard_data, start=1):
    render_row(index, user["name"], user["points"])
