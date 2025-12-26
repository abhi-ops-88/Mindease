import streamlit as st
from src.utils.openai_client import get_ai_response
from src.database.models import (get_conversation_messages, save_message, 
                                create_new_conversation, get_user_conversations)
import os

def ChatInterface():
    # 🔥 PERMANENT DEBUG DASHBOARD (TOP - NEVER DISAPPEARS)
    debug_col1, debug_col2 = st.columns([1,3])
    with debug_col1:
        st.markdown("### 🔍 **DEBUG**")
        
        # API Key check
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success(f"✅ **Key OK** ({len(api_key)} chars)")
        else:
            st.error("❌ **NO API KEY** - Fix Streamlit Secrets!")
        
        # Test button (STAYS VISIBLE)
        if st.button("🧪 **TEST AI NOW**", use_container_width=True):
            try:
                test_response = get_ai_response([{"sender": "user", "content": "test connection"}])
                st.success("🎉 **AI WORKS PERFECTLY!**")
                st.info(f"**Response preview:** {test_response[:100]}...")
            except Exception as e:
                st.error(f"❌ **AI FAILED:** {str(e)}")
                st.info("**Fix:** Check secrets / credits / rate limits")
    
    st.header(f"Welcome back, {st.session_state.username} 👋")
    
    # Sidebar conversations (unchanged)
    with st.sidebar:
        st.subheader("💭 Your Conversations")
        convs = get_user_conversations(st.session_state.user_id)
        
        if convs:
            conv_names = [f"Chat {c['id']} ({c['created_at']})" for c in convs]
            selected
