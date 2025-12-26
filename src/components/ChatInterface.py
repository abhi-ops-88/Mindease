import streamlit as st
from src.utils.openai_client import get_ai_response
from src.database.models import (
    get_conversation_messages,
    save_message,
    create_new_conversation,
    get_user_conversations
)

def ChatInterface():

    if "current_conv_id" not in st.session_state:
        st.session_state.current_conv_id = create_new_conversation(
            st.session_state.user_id
        )

    st.header(f"Welcome back, {st.session_state.username} 👋")

    # ===== Sidebar =====
    with st.sidebar:
        st.subheader("💭 Your Conversations")
        convs = get_user_conversations(st.session_state.user_id)

        labels = ["New Chat"] + [
            f"Chat {c.id} ({c.created_at.strftime('%Y-%m-%d')})"
            for c in convs
        ]

        selected = st.selectbox("Select chat", labels)

        if selected == "New Chat":
            st.session_state.current_conv_id = create_new_conversation(
                st.session_state.user_id
            )
        else:
            st.session_state.current_conv_id = int(selected.split()[1])

    # ===== Messages =====
    messages = get_conversation_messages(st.session_state.current_conv_id)

    for msg in messages:
        with st.chat_message(msg.sender):
            st.markdown(msg.content)

    # ===== Input =====
    if prompt := st.chat_input("How are you feeling today?"):
        save_message(st.session_state.current_conv_id, "user", prompt)

        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):
                history = [
                    {"role": m.sender, "content": m.content}
                    for m in messages
                ]
                history.append({"role": "user", "content": prompt})

                reply = get_ai_response(history)
                st.markdown(reply)
                save_message(
                    st.session_state.current_conv_id,
                    "assistant",
                    reply
                )
