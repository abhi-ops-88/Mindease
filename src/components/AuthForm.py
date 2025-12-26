import streamlit as st
from src.utils.auth import create_user, authenticate_user, hash_password
from src.database.models import get_db_session, User

def AuthForm():
    st.title("🧠 Mental Health Assistant")
    st.markdown("### Please login or sign up")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            success, user = authenticate_user(email, password)
            if success:
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
        
        if st.button("Sign Up", key="signup_btn"):
            success, message = create_user(new_email, username, new_password)
            if success:
                st.success("Account created! Please login.")
            else:
                st.error(message)
