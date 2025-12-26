import openai
import os
from typing import List, Dict

_client = None

def get_openai_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in Streamlit Cloud secrets")
        _client = openai.OpenAI(api_key=api_key)
    return _client

MENTAL_HEALTH_PROMPT = """
You are Sage, compassionate mental health assistant. Validate feelings first. 
CRISIS: Call 988, Text HOME to 741741, 911 emergencies. Never diagnose.
"""

def get_ai_response(messages: List[Dict[str, str]]) -> str:
    try:
        client = get_openai_client()
        context = [{"role": "system", "content": MENTAL_HEALTH_PROMPT}] + messages[-10:]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=context,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI unavailable: {str(e)}. Call 988 for help."
