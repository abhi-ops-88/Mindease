import streamlit as st

def CrisisResourcesBanner():
    st.markdown("""
    <div style='background: #ff4444; color: white; padding: 20px; border-radius: 15px; 
                text-align: center; font-weight: bold; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.3);'>
        <h2>🆘 CRISIS RESOURCES</h2>
        <div style='font-size: 18px; line-height: 1.6;'>
            📞 <strong>988 Suicide & Crisis Lifeline</strong> (Call or text 988)<br>
            📱 <strong>Crisis Text Line:</strong> Text HOME to 741741<br>
            🚨 <strong>EMERGENCY:</strong> Call 911 immediately
        </div>
    </div>
    """, unsafe_allow_html=True)
