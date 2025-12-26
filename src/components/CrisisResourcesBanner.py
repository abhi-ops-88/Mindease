import streamlit as st

def CrisisResourcesBanner():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff4444, #cc0000); 
                color: white; padding: 20px; border-radius: 15px; 
                text-align: center; font-weight: bold; margin: 20px 0; 
                box-shadow: 0 8px 16px rgba(255,68,68,0.3);'>
        <h2 style='margin: 0;'>🆘 CRISIS RESOURCES</h2>
        <div style='font-size: 18px; line-height: 1.6; margin-top: 10px;'>
            📞 <strong>988 Suicide & Crisis Lifeline</strong> (Call or text 988)<br>
            📱 <strong>Crisis Text Line:</strong> Text HOME to 741741<br>
            🚨 <strong>EMERGENCY:</strong> Call 911 immediately
        </div>
    </div>
    """, unsafe_allow_html=True)
