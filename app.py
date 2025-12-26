import streamlit as st
import sqlite3
import hashlib
import openai
from datetime import datetime
import os

st.set_page_config(page_title="Mental Health Assistant", layout="wide", page_icon="🧠")

# OpenAI key
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# Database setup
@st.cache_resource
def init_db():
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  email TEXT UNIQUE, username TEXT UNIQUE, password_hash TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS conversations 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_email TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  conversation_id INTEGER, sender TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, username, password):
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
                 (email, username, hash_password(password)))
        conn.commit()
        return True, "Success"
    except:
        return False, "Email or username exists"
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE email=? AND password_hash=?",
             (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user is not None, user[0] if user else None

# Mental health prompt
MENTAL_HEALTH_PROMPT = """You are Sage, a compassionate mental health assistant. 
Always validate feelings, be empathetic, encourage professional help when needed.
CRISIS: 988 Suicide Lifeline, Text HOME to 741741, 911 emergencies."""

# Gradient + Crisis banner
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, #ff4444, #cc0000); 
            color: white; padding: 20px; border-radius: 15px; 
            text-align: center; font-weight: bold; margin: 20px 0;'>
    <h2>🆘 CRISIS RESOURCES</h2>
    📞 988 Suicide Lifeline | 📱 Text HOME to 741741 | 🚨 Call 911
</div>
""", unsafe_allow_html=True)

# Auth
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
    st.session_state.username = None

if not st.session_state.user_email:
    st.title("🧠 Mental Health Assistant")
    tab1, tab2 = st.tabs(["🔑 Login", "➕ Sign Up"])
    
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, username = authenticate_user(email, password)
            if success:
                st.session_state.user_email = email
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Wrong credentials")
    
    with tab2:
        email = st.text_input("Email", key="signup_email")
        username = st.text_input("Username", key="signup_user")
        password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Create Account"):
            success, msg = create_user(email, username, password)
            if success:
                st.success("✅ Account created! Login above.")
            else:
                st.error(f"❌ {msg}")
else:
    # Chat interface
    st.header(f"Hi {st.session_state.username}! 👋")
    
    # Get conversations
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    c.execute("SELECT id, created_at FROM conversations WHERE user_email=? ORDER BY created_at DESC LIMIT 10",
             (st.session_state.user_email,))
    convs = c.fetchall()
    conn.close()
    
    # Sidebar
    with st.sidebar:
        st.subheader("💭 Conversations")
        if convs:
            conv_options = {f"Chat {id} ({time})": id for id, time in convs}
            selected = st.selectbox("Select:", ["New Chat"] + list(conv_options.keys()))
            if selected == "New Chat":
                conn = sqlite3.connect('mental_health.db')
                c = conn.cursor()
                c.execute("INSERT INTO conversations (user_email, created_at) VALUES (?, ?)",
                         (st.session_state.user_email, datetime.now().strftime("%Y-%m-%d %H:%M")))
                current_conv_id = c.lastrowid
                conn.commit()
                conn.close()
            else:
                current_conv_id = conv_options[selected]
        else:
            current_conv_id = None
        
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()
    
    if 'current_conv_id' not in st.session_state:
        st.session_state.current_conv_id = current_conv_id or 1
    
    # Messages
    conn = sqlite3.connect('mental_health.db')
    c = conn.cursor()
    c.execute("SELECT sender, content FROM messages WHERE conversation_id=? ORDER BY timestamp",
             (st.session_state.current_conv_id,))
    messages = c.fetchall()
    conn.close()
    
    # Display chat
    for sender, content in messages:
        with st.chat_message(sender):
            st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("How are you feeling today?"):
        # User message
        conn = sqlite3.connect('mental_health.db')
        c = conn.cursor()
        c.execute("INSERT INTO messages (conversation_id, sender, content, timestamp) VALUES (?, ?, ?, ?)",
                 (st.session_state.current_conv_id, "user", prompt, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()
        conn.close()
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "system", "content": MENTAL_HEALTH_PROMPT}] + 
                                [{"role": "user" if m[0]=="user" else "assistant", "content": m[1]} for m in messages] + 
                                [{"role": "user", "content": prompt}]
                    )
                    ai_reply = response.choices[0].message.content
                    
                    conn = sqlite3.connect('mental_health.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO messages (conversation_id, sender, content, timestamp) VALUES (?, ?, ?, ?)",
                             (st.session_state.current_conv_id, "assistant", ai_reply, datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    conn.close()
                    
                    st.markdown(ai_reply)
                except:
                    st.error("AI temporarily unavailable. Call 988 for help.")
        st.rerun()
