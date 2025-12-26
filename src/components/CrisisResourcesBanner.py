import streamlit as st

def CrisisResourcesBanner():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff4444, #cc0000); 
                color: white; padding: 20px; border-radius: 15px; 
                text-align: center; font-weight: bold; margin: 20px 0; 
                box-shadow: 0 8px 16px rgba(255,68,68,0.3);'>
        <h2>🆘 CRISIS RESOURCES</h2>
        <div style='font-size: 18px;'>
            📞 988 Suicide & Crisis Lifeline | 📱 Text HOME to 741741 | 🚨 Call 911
        </div>
    </div>
    """, unsafe_allow_html=True)
