import streamlit as st
import sys
import os

# -----------------------------
# PATH FIX (Streamlit Cloud)
# -----------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

# -----------------------------
# PAGE CONFIG (MUST BE FIRST)
# -----------------------------
st.set_page_config(
    page_title="Mental Health Assistant",
    layout="wide",
    page_icon="🧠",
)

# -----------------------------
# IMPORTS
# -----------------------------
from src.components.AuthForm import AuthForm
from src.components.CrisisResourcesBanner import CrisisResourcesBanner
from src.components.ChatInterface import ChatInterface
from src.database import init_db   # 👈 IMPORTANT (not .models)

# -----------------------------
# INIT DATABASE (ONCE)
# -----------------------------
init_db()

# -----------------------------
# GLOBAL STYLES
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None

# -----------------------------
# APP FLOW
# -----------------------------
if not st.session_state.authenticated:
    AuthForm()
else:
    CrisisResourcesBanner()
    st.divider()
    ChatInterface()
