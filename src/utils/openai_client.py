import openai
import streamlit as st
import os
from typing import List, Dict

# 🔥 DEBUG VERSION - Shows exactly what's happening
def debug_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 DEBUG INFO")
    st.sidebar.markdown(f"**API Key loaded:** {'✅ YES' if api_key else '❌ NO'}")
    st.sidebar.markdown(f"**Key length:** {len(api_key) if api_key else 0}")
    if api_key:
        st.sidebar.success("✅ Key format correct!")
    else:
        st.sidebar.error("❌ Fix Streamlit Cloud Secrets!")
    return api_key

_client = None

def get_openai_client():
    global _client
    if _client is None:
        api_key = debug_api_key()  # 🔥 Shows debug info
        if not api_key:
            raise ValueError("OPENAI_API_KEY missing from Streamlit Cloud secrets")
        _client = openai.OpenAI(api_key=api_key)
    return _client

MENTAL_HEALTH_SYSTEM_PROMPT = """
You are Sage, a compassionate mental health assistant. ALWAYS:
1. Validate feelings first
2. Be empathetic
3. Mention crisis resources when needed
CRISIS: 988 Lifeline, Text HOME to 741741, 911 emergencies.
"""

def get_ai_response(messages: List[Dict[str, str]]) -> str:
    try:
        client = get_openai_client()
        context = messages[-10:]
        full_context = [{"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT}] + context
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ Your key has access
            messages=full_context,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"AI Error details: {str(e)}")
        return "AI temporarily unavailable. Call 988 for immediate help."
