import streamlit as st
from src.utils.openai_client import get_ai_response
from src.database.models import (get_conversation_messages, save_message, 
                                create_new_conversation, get_user_conversations)

def ChatInterface():
    # Initialize conversation if needed
    if 'current_conv_id' not in st.session_state:
        st.session_state.current_conv_id = create_new_conversation(st.session_state.user_id)
    
    st.header(f"Welcome back, {st.session_state.username} 👋")
    
    # Sidebar - Conversations
    with st.sidebar:
        st.subheader("💭 Your Conversations")
        convs = get_user_conversations(st.session_state.user_id)
        
        if convs:
            conv_names = [f"Chat {c['id']} ({c['created_at']})" for c in convs]
            selected = st.selectbox("Select chat:", ["New Chat"] + conv_names, key="conv_select")
            
            if selected == "New Chat":
                st.session_state.current_conv_id = create_new_conversation(st.session_state.user_id)
            else:
                conv_id = int(selected.split()[1][0])
                st.session_state.current_conv_id = conv_id
        else:
            st.info("No conversations yet. Start chatting!")
    
    # Chat display
    current_conv_id = st.session_state.current_conv_id
    messages = get_conversation_messages(current_conv_id)
    
    chat_container = st.container()
    with chat_container:
        for msg in messages:
            if msg['sender'] == 'user':
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #8B9DC3, #667eea); 
                           color: white; padding: 15px; border-radius: 20px 20px 5px 20px; 
                           margin: 10px 60px 10px 10px; max-width: 70%;'>
                    <strong>You:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: #E0E0E0; color: #333; padding: 15px; 
                           border-radius: 20px 20px 20px 5px; margin: 10px 10px 10px 60px; 
                           max-width: 70%;'>
                    <strong>Sage:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("How are you feeling today?..."):
        # Save & display user message
        save_message(current_conv_id, "user", prompt)
        st.chat_message("user").markdown(prompt)
        
        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):
                # Convert messages for OpenAI
                openai_messages = [{"role": "user" if m["sender"] == "user" else "assistant", 
                                  "content": m["content"]} for m in messages + [{"sender": "user", "content": prompt}]]
                
                response = get_ai_response(openai_messages)
                st.markdown(response)
                save_message(current_conv_id, "assistant", response)
        
        st.rerun()
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
