import openai
import streamlit as st
import os
from typing import List, Dict

# 🔥 LAZY INITIALIZATION - No crash on import
_client = None

def get_openai_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in Streamlit Cloud secrets")
        _client = openai.OpenAI(api_key=api_key)
    return _client

MENTAL_HEALTH_SYSTEM_PROMPT = """
You are Sage, a compassionate mental health assistant. ALWAYS:
1. Validate feelings first - "I hear you're feeling..."
2. Be empathetic, never judgmental
3. Encourage professional help when needed
4. NEVER diagnose or prescribe
5. Mention crisis resources for serious issues

CRISIS RESOURCES:
- 📞 988 Suicide & Crisis Lifeline (Call/text 988)
- 📱 Crisis Text Line: Text HOME to 741741
- 🚨 911 for emergencies
"""

def get_ai_response(messages: List[Dict[str, str]]) -> str:
    try:
        client = get_openai_client()
        context = messages[-10:]  # Last 10 messages
        full_context = [{"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT}] + context
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=full_context,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"AI temporarily unavailable: {str(e)}")
        return "I'm here for you. For urgent help: Call 988 or text HOME to 741741."
