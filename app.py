import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath("src"))

# Safe database reset for Streamlit Cloud
if os.path.exists('mental_health.db'):
    os.remove('mental_health.db')

from src.components.AuthForm import AuthForm
from src.components.CrisisResourcesBanner import CrisisResourcesBanner
from src.components.ChatInterface import ChatInterface
from src.database.models import init_db

# Initialize database (safe now)
init_db()

st.set_page_config(page_title="Mental Health Assistant", layout="wide", page_icon="🧠")

# Gradient background
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
.stApp {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
</style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None

if not st.session_state.authenticated:
    AuthForm()
else:
    CrisisResourcesBanner()
    st.divider()
    ChatInterface()
    
    # Sidebar logout
    with st.sidebar:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
