import openai
import streamlit as st

openai.api_key = st.secrets.get("OPENAI_API_KEY")

MENTAL_HEALTH_PROMPT = """You are Sage, a compassionate mental health assistant. 
Always validate feelings first. Be empathetic. Encourage professional help.
CRISIS RESOURCES: 988 Suicide Lifeline, Text HOME to 741741, 911 emergencies."""

def get_ai_response(messages):
    try:
        full_context = [{"role": "system", "content": MENTAL_HEALTH_PROMPT}]
        full_context.extend([{"role": "user" if m["sender"] == "user" else "assistant", "content": m["content"]} for m in messages[-10:]])
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=full_context,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except:
        return "I'm here for you. For urgent help: Call 988 or text HOME to 741741."
