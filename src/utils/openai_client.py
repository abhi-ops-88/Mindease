from groq import Groq

SYSTEM_PROMPT = (
    "You are Sage, a calm, empathetic mental health assistant. "
    "Respond naturally, with warmth. Ask relevant follow-up questions. "
    "Do NOT repeat the same sentence."
)

def get_ai_response(messages):
    try:
        client = Groq()  # uses GROQ_API_KEY from Streamlit secrets

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.7,
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Only fallback if AI truly fails
        return (
            "I’m here with you. It sounds like something has been weighing on you. "
            "Do you want to tell me more about it?"
        )
