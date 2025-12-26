from openai import OpenAI

# The OpenAI client automatically reads OPENAI_API_KEY
# from the environment (Streamlit secrets)
client = OpenAI()

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
            "I'm really sorry you're having a hard day. 💙\n\n"
            "I'm here with you. If things feel overwhelming or unsafe, "
            "please consider calling **988** (US Suicide & Crisis Lifeline)."
        )
