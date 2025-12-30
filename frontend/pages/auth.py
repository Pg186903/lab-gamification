from __future__ import annotations

import streamlit as st
from utils.api_client import signup_user, login_user

st.set_page_config(page_title="Stomata Labs | Auth", layout="centered")

st.title("🧪 Stomata Labs")
st.caption("Gamified AI Adoption Platform")

tab_login, tab_signup = st.tabs(["🔐 Login", "✨ Sign Up"])

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
with tab_login:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")

    if login_submit:
        token = login_user(email, password)
        if token:
            st.session_state.access_token = token
            st.success("Login successful!")
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Invalid email or password.")

# ---------------------------------------------------
# SIGNUP
# ---------------------------------------------------
with tab_signup:
    with st.form("signup_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pwd")
        signup_submit = st.form_submit_button("Create Account")

    if signup_submit:
        if not full_name or not email or not password:
            st.error("All fields are required.")
        else:
            user = signup_user(
                {
                    "full_name": full_name,
                    "email": email,
                    "password": password,
                }
            )
            if user:
                # AUTO LOGIN AFTER SIGNUP
                token = login_user(email, password)
                st.session_state.access_token = token
                st.success("Account created and logged in!")
                st.switch_page("pages/dashboard.py")
            else:
                st.error("Signup failed.")
