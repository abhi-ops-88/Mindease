from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_ai_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception as e:
        return (
            "I'm really sorry you're having a hard day. "
            "I'm here with you, even if things feel heavy right now.\n\n"
            "If you're feeling overwhelmed or unsafe, please consider calling "
            "**988** (US Suicide & Crisis Lifeline). 💙"
        )
