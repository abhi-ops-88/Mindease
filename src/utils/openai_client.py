import openai
import streamlit as st
from typing import List, Dict

# Load OpenAI key from secrets
openai.api_key = st.secrets.get("OPENAI_API_KEY")

MENTAL_HEALTH_SYSTEM_PROMPT = """
You are Sage, a compassionate mental health assistant. Your responses should ALWAYS:

1. **Validate feelings first** - "I hear you're feeling..."
2. **Be empathetic** - Never judgmental
3. **Encourage professional help** when needed
4. **NEVER diagnose** or prescribe medication
5. **Mention crisis resources** for serious issues

CRISIS RESOURCES (mention when appropriate):
- 📞 988 Suicide & Crisis Lifeline (Call/text 988)
- 📱 Crisis Text Line: Text HOME to 741741  
- 🚨 911 for emergencies

Structure every response:
1. Acknowledge their feelings
2. Offer support
3. Ask gentle follow-up question
4. Suggest coping strategies
"""

def get_ai_response(messages: List[Dict[str, str]]) -> str:
    """
    Get AI response for mental health chat
    """
    try:
        # Build full context (last 20 messages max)
        context = messages[-20:] if len(messages) > 20 else messages
        
        # Add system prompt at start
        full_context = [{"role": "system", "content": MENTAL_HEALTH_SYSTEM_PROMPT}] + context
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Fast & cheap
            messages=full_context,
            max_tokens=500,
            temperature=0.7,
            top_p=0.9
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.error(f"AI service temporarily unavailable: {str(e)}")
        return "I'm here for you. For urgent help, please call 988 or text HOME to 741741."
