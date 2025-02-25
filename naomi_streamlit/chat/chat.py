import streamlit as st

from naomi_streamlit.chat.assistant import draw_assistant_message, draw_draft_assistant_message
from naomi_streamlit.chat.user_input import draw_user_message
from naomi_streamlit.db import (
    DEFAULT_CONVERSATION_ID,
    Message,
    MessageModel,
    add_message_to_db,
    fetch_messages,
    session_scope,
)


def draw_messages(messages: list[MessageModel], session):
    for message in messages:
        role = message.payload["role"]
        with st.chat_message("user" if role == "user" else "assistant"):
            if role == "user":
                draw_user_message(message, session)
            else:
                draw_assistant_message(message, session)


def draw_chat():
    st.header("💬 Chat")

    with session_scope() as session:
        messages = fetch_messages(session, DEFAULT_CONVERSATION_ID)
        draw_messages(messages, session)

    if prompt := st.chat_input("Type your message here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with session_scope() as session:
            add_message_to_db(Message.from_user_input(prompt), DEFAULT_CONVERSATION_ID, session)
            with st.chat_message("assistant"):
                draw_draft_assistant_message(DEFAULT_CONVERSATION_ID, session)
                st.rerun()
