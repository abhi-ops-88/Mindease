import streamlit as st
from src.utils.auth import create_user, authenticate_user
from src.database.models import User  # ✅ FIXED: Removed get_db_session

def AuthForm():
    st.title("🧠 Mental Health Assistant")
    st.markdown("### Welcome! Please login or create an account")
    
    tab1, tab2 = st.tabs(["🔑 Login", "➕ Sign Up"])
    
    with tab1:
        col1, col2 = st.columns([3,1])
        with col1:
            email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        with col2:
            password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary"):
            success, result = authenticate_user(email, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_id = result.id
                st.session_state.username = result.username
                st.success(f"Welcome back, {result.username}! 👋")
                st.rerun()
            else:
                st.error("❌ Invalid email or password")
    
    with tab2:
        col1, col2 = st.columns([1,3])
        with col1:
            new_email = st.text_input("Email", key="signup_email")
        with col2:
            username = st.text_input("Username", key="signup_username")
            new_password = st.text_input("Password", type="password", key="signup_password")
        
        if st.button("Create Account"):
            success, message = create_user(new_email, username, new_password)
            if success:
                st.success("✅ Account created! Please login above.")
            else:
                st.error(f"❌ {message}")
