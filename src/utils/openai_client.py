import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]

    except Exception:
        return (
            "I'm really sorry you're having a tough moment 💙\n\n"
            "If you feel unsafe, please call **988** (US Suicide & Crisis Lifeline). "
            "You’re not alone."
        )
