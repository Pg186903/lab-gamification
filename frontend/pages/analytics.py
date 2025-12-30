"""
Analytics page for the Stomata Labs gamified frontend.
Displays feature usage statistics.
"""

from __future__ import annotations

from typing import List, Dict

import streamlit as st

from utils.api_client import log_event

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.title("📊 Analytics")
st.markdown(
    "<p class='neon-subtitle'>Understand how features are being used</p>",
    unsafe_allow_html=True,
)

token = st.session_state.get("access_token")

if not token:
    st.error("You are not authenticated.")
    st.stop()

# Log page open
log_event(token, feature="analytics", action="open")

# ---------------------------------------------------------
# Dummy analytics data (replace with backend call later)
# ---------------------------------------------------------
analytics_data: List[Dict[str, int]] = [
    {"feature": "quiz", "count": 120},
    {"feature": "leaderboard", "count": 95},
    {"feature": "dashboard", "count": 150},
    {"feature": "anomaly", "count": 60},
]

# ---------------------------------------------------------
# Render chart
# ---------------------------------------------------------
features = [item["feature"] for item in analytics_data]
counts = [item["count"] for item in analytics_data]

st.markdown("## 🔍 Feature Usage Overview")

chart_data = {
    "Feature": features,
    "Usage Count": counts,
}

st.bar_chart(chart_data)
