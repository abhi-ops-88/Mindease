import os
from groq import Groq

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = (
    "You are Sage, a calm, empathetic mental health support assistant. "
    "Listen carefully, respond warmly, and ask gentle follow-up questions. "
    "Do NOT repeat crisis hotlines unless the user explicitly expresses self-harm or suicidal intent."
)

def get_ai_response(messages):
    """
    messages = [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
    """

    try:
        chat = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return chat.choices[0].message.content.strip()

    except Exception as e:
        # SAFE fallback (no crashes, no spam)
        return (
            "I'm here with you. "
            "It sounds like something has been weighing on you — "
            "do you want to tell me more about what's been happening?"
        )
