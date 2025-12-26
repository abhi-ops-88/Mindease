import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath("src"))

from src.components.AuthForm import AuthForm
from src.components.ChatInterface import ChatInterface
from src.database.models import init_db

st.set_page_config(
    page_title="Mental Health Assistant",
    layout="wide",
    page_icon="🧠"
)

init_db()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None

if not st.session_state.authenticated:
    AuthForm()
else:
    ChatInterface()

    with st.sidebar:
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()
