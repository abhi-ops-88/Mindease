import streamlit as st
from src.utils.openai_client import get_ai_response
from src.database.models import (
    get_conversation_messages,
    save_message,
    create_conversation,
    get_user_conversations,
)


def ChatInterface():
    # =====================================================
    # INITIALIZE CONVERSATION (store ONLY conversation_id)
    # =====================================================
    if "current_conv_id" not in st.session_state:
        conv = create_conversation(st.session_state.user_id)
        st.session_state.current_conv_id = conv.id

    st.header(f"Welcome back, {st.session_state.username} 👋")

    # =====================================================
    # SIDEBAR - CONVERSATION LIST
    # =====================================================
    with st.sidebar:
        st.subheader("💭 Your Conversations")

        convs = get_user_conversations(st.session_state.user_id)

        if convs:
            conv_labels = [
                f"Chat {c.id} ({c.created_at.strftime('%Y-%m-%d %H:%M')})"
                for c in convs
            ]

            selected = st.selectbox(
                "Select chat",
                ["New Chat"] + conv_labels,
            )

            if selected == "New Chat":
                conv = create_conversation(st.session_state.user_id)
                st.session_state.current_conv_id = conv.id
                st.rerun()
            else:
                conv_id = int(selected.split()[1])
                st.session_state.current_conv_id = conv_id
        else:
            st.info("No conversations yet.")

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

    # =====================================================
    # CHAT DISPLAY
    # =====================================================
    current_conv_id = st.session_state.current_conv_id
    messages = get_conversation_messages(current_conv_id)

    for msg in messages:
        with st.chat_message(msg.sender):
            st.markdown(msg.content)

    # =====================================================
    # CHAT INPUT
    # =====================================================
    if prompt := st.chat_input("How are you feeling today?"):
        # Save user message
        save_message(current_conv_id, "user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        # Build OpenAI message history
        openai_messages = [
            {"role": m.sender, "content": m.content} for m in messages
        ]
        openai_messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):
                response = get_ai_response(openai_messages)
                st.markdown(response)
                save_message(current_conv_id, "assistant", response)

        st.rerun()
