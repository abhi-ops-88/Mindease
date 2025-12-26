import streamlit as st
from src.components.AuthForm import AuthForm
from src.components.CrisisResourcesBanner import CrisisResourcesBanner
from src.components.ChatInterface import ChatInterface
from src.database.models import init_db

# Initialize database
init_db()

st.set_page_config(page_title="Mental Health Assistant", layout="wide", page_icon="🧠")

# Gradient background
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
</style>
""", unsafe_allow_html=True)

# Main app layout
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    AuthForm()
else:
    CrisisResourcesBanner()
    st.divider()
    ChatInterface()
