import os
import openai

# Load API key from environment (Streamlit Cloud compatible)
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "You are Sage, a calm, empathetic mental health support assistant. "
    "You listen carefully, respond with compassion, and never diagnose. "
    "Offer grounding advice gently and ask thoughtful follow-up questions."
)

def get_ai_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            temperature=0.7,
        )

        return response.choices[0].message["content"]

    except Exception as e:
        # Show real error instead of masking it
        return f"AI unavailable: {str(e)}"
