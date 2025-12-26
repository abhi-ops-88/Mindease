import os
from openai import OpenAI

# 🔥 STREAMLIT CLOUD FIX — REMOVE PROXIES
for key in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(key, None)

client = OpenAI()

def get_ai_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception:
        return (
            "I'm really sorry you're having a hard day. 💙\n\n"
            "I'm here with you. If things feel overwhelming or unsafe, "
            "please consider calling **988** (US Suicide & Crisis Lifeline)."
        )
