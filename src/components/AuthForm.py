import streamlit as st
from src.utils.auth import create_user, authenticate_user


def AuthForm():
    st.title("🧠 Mental Health Assistant")

    tab1, tab2 = st.tabs(["🔑 Login", "➕ Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            user = authenticate_user(email, password)

            if user:
                st.session_state.authenticated = True
                st.session_state.user_id = user.id
                st.session_state.username = user.username
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_email = st.text_input("Email", key="signup_email")
        username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            user = create_user(new_email, username, new_password)

            if user:
                st.success("Account created! Please log in.")
            else:
                st.error("Email or username already exists")
