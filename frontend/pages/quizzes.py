"""
Quiz page for the Stomata Labs gamified frontend.
Allows users to attempt quizzes and logs their activity.
"""

from __future__ import annotations

from typing import Dict

import streamlit as st

from utils.api_client import log_event

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.title("🧪 Knowledge Quizzes")
st.markdown(
    "<p class='neon-subtitle'>Sharpen your skills and earn points</p>",
    unsafe_allow_html=True,
)

token = st.session_state.get("access_token")

if not token:
    st.error("You are not authenticated.")
    st.stop()

# Log quiz page open
log_event(token, feature="quiz", action="open")

# ---------------------------------------------------------
# Dummy quiz data (replace with API call later)
# ---------------------------------------------------------
QUIZ_QUESTIONS: Dict[str, Dict[str, str]] = {
    "q1": {
        "question": "What does maintaining stable oscillation prevent?",
        "A": "System downtime",
        "B": "Energy loss",
        "C": "Signal distortion",
        "D": "All of the above",
        "answer": "D",
    },
    "q2": {
        "question": "Which action earns maximum points?",
        "A": "Ignoring alerts",
        "B": "Handling anomalies quickly",
        "C": "Skipping shifts",
        "D": "Closing the dashboard",
        "answer": "B",
    },
}

# ---------------------------------------------------------
# Quiz Form
# ---------------------------------------------------------
with st.form("quiz_form"):
    user_answers: Dict[str, str] = {}

    for qid, data in QUIZ_QUESTIONS.items():
        st.markdown(f"**{data['question']}**")
        choice = st.radio(
            label="",
            options=["A", "B", "C", "D"],
            format_func=lambda x, opts=data: f"{x}: {opts[x]}",
            key=qid,
        )
        user_answers[qid] = choice

    submitted = st.form_submit_button("Submit Quiz")

# ---------------------------------------------------------
# Evaluate Quiz
# ---------------------------------------------------------
if submitted:
    score = 0
    for qid, selected in user_answers.items():
        if selected == QUIZ_QUESTIONS[qid]["answer"]:
            score += 1

    log_event(
        token,
        feature="quiz",
        action="submit",
        metadata={"score": score},
    )

    st.success(f"🎉 You scored {score} / {len(QUIZ_QUESTIONS)}")
