import os
import streamlit as st
from groq import Groq

# -------------------------------------------------
# 🔥 FIX: Disable proxy variables (Streamlit Cloud)
# -------------------------------------------------
for key in [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "http_proxy",
    "https_proxy",
]:
    os.environ.pop(key, None)

# -------------------------------------------------
# System prompt
# -------------------------------------------------
SYSTEM_PROMPT = """
You are Sage, a calm, empathetic mental health assistant.
Speak naturally and warmly.
Ask thoughtful follow-up questions.
Never repeat the same sentence.
Do not give medical diagnoses.
Encourage professional help when appropriate.
"""

# -------------------------------------------------
# AI Response
# -------------------------------------------------
def get_ai_response(messages):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.8,
            max_tokens=300,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"AI Error: {e}")
        return (
            "I’m really glad you shared that with me. "
            "Do you want to tell me a bit more about what today has been like for you?"
        )
