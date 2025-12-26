import os
import streamlit as st
import httpx
from groq import Groq

# -------------------------------------------------
# 🔥 HARD FIX: Custom HTTP client (no proxies)
# -------------------------------------------------
http_client = httpx.Client(
    proxies=None,
    timeout=30.0,
)

SYSTEM_PROMPT = """
You are Sage, a calm, empathetic mental health assistant.
Speak naturally and warmly.
Ask thoughtful follow-up questions.
Never repeat the same sentence.
Do not give medical diagnoses.
Encourage professional help when appropriate.
"""

def get_ai_response(messages):
    try:
        client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
            http_client=http_client,  # 🔥 THIS is the key
        )

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages,
            ],
            temperature=0.85,
            max_tokens=350,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        st.error(f"AI Error: {e}")
        return (
            "I’m really glad you shared that with me. "
            "What part of today has felt the heaviest so far?"
        )
