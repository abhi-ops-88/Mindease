import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath("src"))

st.set_page_config(page_title="Mental Health Assistant", layout="wide", page_icon="🧠")

from src.components.AuthForm import AuthForm
from src.components.CrisisResourcesBanner import CrisisResourcesBanner
from src.components.ChatInterface import ChatInterface
from src.database.models import init_db

init_db()

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
    
    with st.sidebar:
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()
