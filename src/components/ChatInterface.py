import streamlit as st
from src.utils.openai_client import get_ai_response
from src.database import (
    create_conversation,
    get_user_conversations,
    get_conversation_messages,
    save_message,
)

def ChatInterface():
    # =========================
    # INIT CONVERSATION
    # =========================
    if "current_conv_id" not in st.session_state:
        st.session_state.current_conv_id = create_conversation(
            st.session_state.user_id
        )

    st.header(f"Welcome back, {st.session_state.username} 👋")

    # =========================
    # SIDEBAR
    # =========================
    with st.sidebar:
        st.subheader("💭 Your Conversations")

        convs = get_user_conversations(st.session_state.user_id)

        if convs:
            labels = [f"Chat {c.id} ({c.created_at:%Y-%m-%d})" for c in convs]
            selected = st.selectbox("Select chat", ["New Chat"] + labels)

            if selected == "New Chat":
                st.session_state.current_conv_id = create_conversation(
                    st.session_state.user_id
                )
                st.rerun()
            else:
                conv_id = int(selected.split()[1])
                st.session_state.current_conv_id = conv_id

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.rerun()

    # =========================
    # CHAT HISTORY
    # =========================
    messages = get_conversation_messages(st.session_state.current_conv_id)

    for msg in messages:
        with st.chat_message(msg["sender"]):
            st.markdown(msg["content"])

    # =========================
    # CHAT INPUT
    # =========================
    if prompt := st.chat_input("How are you feeling today?"):
        save_message(st.session_state.current_conv_id, "user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):
                chat_context = [
                    {"role": m["sender"], "content": m["content"]}
                    for m in messages
                ]
                chat_context.append({"role": "user", "content": prompt})

                response = get_ai_response(chat_context)
                st.markdown(response)
                save_message(
                    st.session_state.current_conv_id,
                    "assistant",
                    response,
                )

        st.rerun()
