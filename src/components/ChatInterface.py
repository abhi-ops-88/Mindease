import streamlit as st
from src.utils.openai_client import get_ai_response
# from src.database.models import (
#     get_conversation_messages,
#     save_message,
#     create_conversation,
#     get_user_conversations
# )

from src.database import (
    get_conversation_messages,
    save_message,
    create_new_conversation,
    get_user_conversations
)

def ChatInterface():
    # Initialize conversation
    if 'current_conv_id' not in st.session_state:
        # st.session_state.current_conv_id = create_conversation(
        #     st.session_state.user_id
        st.session_state.current_conv_id = create_new_conversation(
    st.session_state.user_id
)

        )

    st.header(f"Welcome back, {st.session_state.username} 👋")

    # Sidebar
    with st.sidebar:
        st.subheader("💭 Your Conversations")
        convs = get_user_conversations(st.session_state.user_id)

        if convs:
            conv_names = [f"Chat {c.id} ({c.created_at})" for c in convs]
            selected = st.selectbox("Select chat:", ["New Chat"] + conv_names)

            if selected == "New Chat":
                st.session_state.current_conv_id = create_conversation(
                    st.session_state.user_id
                )
            else:
                conv_id = int(selected.split()[1])
                st.session_state.current_conv_id = conv_id
        else:
            st.info("No conversations yet.")

    # Chat display
    current_conv_id = st.session_state.current_conv_id
    messages = get_conversation_messages(current_conv_id)

    for msg in messages:
        with st.chat_message(msg["sender"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("How are you feeling today?..."):
        save_message(current_conv_id, "user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):
                openai_messages = [
                    {"role": msg["sender"], "content": msg["content"]}
                    for msg in messages
                ]
                openai_messages.append(
                    {"role": "user", "content": prompt}
                )

                response = get_ai_response(openai_messages)
                st.markdown(response)
                save_message(current_conv_id, "assistant", response)

        st.rerun()

    # Logout
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
