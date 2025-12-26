import streamlit as st
from src.utils.openai_client import get_ai_response
from src.database.models import (
    get_conversation_messages,
    save_message,
    create_conversation,
    get_user_conversations,
)


def ChatInterface():

    # -----------------------------
    # SAFETY CHECK
    # -----------------------------
    if "user_id" not in st.session_state:
        st.error("User not authenticated.")
        return

    # -----------------------------
    # INITIALIZE CONVERSATION ONCE
    # -----------------------------
    if "current_conv_id" not in st.session_state:
        conv = create_conversation(st.session_state.user_id)
        st.session_state.current_conv_id = conv.id

    st.header(f"Welcome back, {st.session_state.username} 👋")

    # -----------------------------
    # SIDEBAR – CONVERSATIONS
    # -----------------------------
    with st.sidebar:
        st.subheader("💭 Your Conversations")

        conversations = get_user_conversations(st.session_state.user_id)

        if conversations:
            labels = [
                f"Chat {c.id} ({c.created_at.strftime('%Y-%m-%d %H:%M')})"
                for c in conversations
            ]

            selected = st.selectbox(
                "Select a chat",
                ["New Chat"] + labels,
                key="chat_selector",
            )

            if selected == "New Chat":
                conv = create_conversation(st.session_state.user_id)
                st.session_state.current_conv_id = conv.id
            else:
                st.session_state.current_conv_id = int(selected.split()[1])

        else:
            st.info("No conversations yet.")

    # -----------------------------
    # LOAD MESSAGES
    # -----------------------------
    conv_id = st.session_state.current_conv_id
    messages = get_conversation_messages(conv_id)

    # -----------------------------
    # DISPLAY CHAT
    # -----------------------------
    for msg in messages:
        with st.chat_message(msg.sender):
            st.markdown(msg.content)

    # -----------------------------
    # CHAT INPUT
    # -----------------------------
    prompt = st.chat_input("How are you feeling today?")

    if prompt:
        # Save user message
        save_message(conv_id, "user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):
                history = [
                    {"role": m.sender, "content": m.content}
                    for m in messages
                ]
                history.append({"role": "user", "content": prompt})

                response = get_ai_response(history)
                st.markdown(response)

                save_message(conv_id, "assistant", response)
