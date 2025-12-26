import streamlit as st
from src.utils.database import get_conversations, create_conversation, get_messages, save_message
from src.utils.openai_client import get_ai_response

def ChatInterface():
    st.header(f"Welcome back, {st.session_state.username} 👋")
    
    # Sidebar
    with st.sidebar:
        st.subheader("💭 Your Conversations")
        convs = get_conversations(st.session_state.user_email)
        
        if convs:
            conv_options = {f"Chat {c['id']} ({c['created_at']})": c['id'] for c in convs}
            selected = st.selectbox("Select:", ["New Chat"] + list(conv_options.keys()))
            
            if selected == "New Chat":
                st.session_state.current_conv_id = create_conversation(st.session_state.user_email)
            else:
                st.session_state.current_conv_id = conv_options[selected]
        else:
            st.session_state.current_conv_id = create_conversation(st.session_state.user_email)
    
    # Chat
    current_conv_id = st.session_state.current_conv_id
    messages = get_messages(current_conv_id)
    
    chat_container = st.container()
    with chat_container:
        for msg in messages:
            with st.chat_message(msg['sender']):
                st.markdown(msg['content'])
    
    # Input
    if prompt := st.chat_input("How are you feeling today?..."):
        save_message(current_conv_id, "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):
                response = get_ai_response(messages + [{"sender": "user", "content": prompt}])
                st.markdown(response)
                save_message(current_conv_id, "assistant", response)
        st.rerun()
