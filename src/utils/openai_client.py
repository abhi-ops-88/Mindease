import os
import streamlit as st
from groq import Groq

# -------------------------------------------------
# System prompt (controls personality + behavior)
# -------------------------------------------------

SYSTEM_PROMPT = """
You are Sage, a kind, calm, empathetic mental health assistant.
- Respond naturally and conversationally
- Ask thoughtful follow-up questions
- Never repeat the same response
- Do NOT give medical diagnoses
- Encourage seeking professional help when appropriate
"""

# -------------------------------------------------
# AI response function
# -------------------------------------------------

def get_ai_response(messages):
    """
    messages: list of dicts
    Example:
    [
        {"role": "user", "content": "I feel anxious"},
        {"role": "assistant", "content": "Tell me more"},
    ]
    """

    try:
        # Initialize Groq client
        client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        # Create completion
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.7,
            max_tokens=300,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        # 🔥 IMPORTANT: show real error so debugging is easy
        st.error(f"AI Error: {e}")

        # Safe fallback response (non-repetitive)
        return (
            "I’m really glad you reached out. "
            "Would you like to tell me what’s been weighing on you today?"
        )
