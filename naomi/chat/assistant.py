import logging
from typing import Iterator
import streamlit as st

from naomi.assistant.persistence import generate_and_persist_llm_response
from naomi.db import (
    MessageModel,
    delete_messages_after,
)


def show_llm_response(chunks: Iterator[str], spinner_message: str) -> str:
    with st.spinner(spinner_message):
        return str(st.write_stream(chunks))


def show_llm_generation(chunks: Iterator[str]) -> str:
    return show_llm_response(chunks, "Generating response...")


def show_llm_regeneration(chunks: Iterator[str]) -> str:
    return show_llm_response(chunks, "Regenerating response...")


def draw_assistant_message(existing_message: MessageModel, session):
    message_id = existing_message.id
    col1, col3, col2 = st.columns([3, 1, 1])

    col1.write(message_id)

    if col2.button("🗑️", key=f"delete_{message_id}"):
        logging.info(f"Deleting messages from {existing_message.id}")
        delete_messages_after(session, existing_message)
        st.rerun()
        return

    if not col3.button("🔃", key=f"regenerate_{message_id}"):
        st.markdown(existing_message.payload.body)
        return

    generate_and_persist_llm_response(existing_message, show_llm_generation, session)


def draw_draft_assistant_message(conversation_id: int, session):
    col1, _ = st.columns([1, 2])

    col1.write("draft")

    message = MessageModel.from_llm_response(conversation_id, "")
    generate_and_persist_llm_response(message, show_llm_generation, session)
