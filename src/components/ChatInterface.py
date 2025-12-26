import streamlit as st
from src.utils.openai_client import get_ai_response
from src.database.models import get_conversation_messages, save_message, create_new_conversation

def ChatInterface():
    if 'current_conv_id' not in st.session_state:
        st.session_state.current_conv_id = create_new_conversation(st.session_state.user_id)
    
    # Load messages
    messages = get_conversation_messages(st.session_state.current_conv_id)
    # ... rest of your code


def ChatInterface():
    st.header(f"Welcome back, {st.session_state.username} 👋")
    
    # Sidebar conversations
    with st.sidebar:
        st.subheader("Your Conversations")
        convs = get_user_conversations(st.session_state.user_id)
        selected = st.selectbox("Select:", ["New Chat"] + [f"Chat {c['id']}" for c in convs])
    
    # Chat messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Chat display with bubbles
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg['sender'] == 'user':
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #8B9DC3, #667eea); 
                           color: white; padding: 15px; border-radius: 20px 20px 5px 20px; 
                           margin: 10px 50px 10px 10px; max-width: 70%;'>
                    <strong>You:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: #E0E0E0; color: #333; padding: 15px; 
                           border-radius: 20px 20px 20px 5px; margin: 10px 10px 10px 50px; 
                           max-width: 70%;'>
                    <strong>Sage:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("How are you feeling today?..."):
        with st.chat_message("user"):
            st.markdown(prompt)
            save_message(st.session_state.current_conv_id, "user", prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Sage is responding..."):
                response = get_ai_response(st.session_state.messages + [{"role": "user", "content": prompt}])
                st.markdown(response)
                save_message(st.session_state.current_conv_id, "assistant", response)
