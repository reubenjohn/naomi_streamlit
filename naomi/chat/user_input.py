import logging
import streamlit as st

from naomi.db import (
    MessageModel,
    delete_messages_after,
)


def draw_user_message(message: MessageModel, session):
    msg = message.payload
    col1, _, col3 = st.columns([3, 1, 1])
    with col1:
        st.write(message.id)
    with col3:
        if st.button("🗑️", key=f"delete_{message.id}"):
            logging.info(f"Deleting messages from {message.id}")
            delete_messages_after(session, message)
            st.rerun()
            return
    st.markdown(msg["content"])
