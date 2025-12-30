"""
Dashboard page for the Stomata Labs gamified frontend.
Shows points, quick actions, and activity logging.
"""

from __future__ import annotations

import streamlit as st

from utils.api_client import log_event

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.title("⚡ Operations Dashboard")
st.markdown(
    "<p class='neon-subtitle'>Track your performance and earn rewards</p>",
    unsafe_allow_html=True,
)

token = st.session_state.get("access_token")

if not token:
    st.error("You are not authenticated.")
    st.stop()

# ---------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------
def neon_card(title: str, content: str) -> None:
    """Render a reusable neon card."""
    st.markdown(
        f"""
        <div class="neon-card">
            <div class="neon-title">{title}</div>
            <div style="font-size:1.2rem;margin-top:0.5rem;">
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# Top Stats Row
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    neon_card("🏆 Total Points", "1,240")

with col2:
    neon_card("🔥 Current Streak", "5 days")

with col3:
    neon_card("🎖 Rank", "Silver")

# ---------------------------------------------------------
# Quick Actions
# ---------------------------------------------------------
st.markdown("## 🎯 Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    if st.button("✔ Completed Shift Smoothly"):
        log_event(token, feature="shift", action="completed_smooth")
        st.success("Nice work! Event logged.")

with action_col2:
    if st.button("⚠️ Handled Anomaly"):
        log_event(token, feature="anomaly", action="handled")
        st.success("Anomaly handling recorded.")

with action_col3:
    if st.button("❌ Missed Check"):
        log_event(token, feature="check", action="missed")
        st.warning("Missed check logged.")

# ---------------------------------------------------------
# Activity Section
# ---------------------------------------------------------
st.markdown("## 🧠 Activity Feed")

neon_card(
    "Latest Highlight",
    "You handled 3 anomalies today. Keep pushing towards Gold rank!",
)
