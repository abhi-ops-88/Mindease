import os
from groq import Groq

SYSTEM_PROMPT = (
    "You are Sage, a calm, empathetic mental health support assistant. "
    "Listen carefully and respond warmly. "
    "Ask gentle follow-up questions. "
    "Only mention emergency resources if the user clearly expresses self-harm intent."
)

def get_ai_response(messages):
    """
    messages = [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
    """

    try:
        # ✅ Create client INSIDE function
        # ✅ Do NOT pass api_key or proxies
        client = Groq()

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.7,
            max_tokens=400,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        # 🔒 Safe fallback — no crashes, no hotline spam
        return (
            "I’m here with you. "
            "It sounds like something has been weighing on you. "
            "Do you want to tell me more about it?"
        )
