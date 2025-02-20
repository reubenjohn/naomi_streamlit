# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import logging
from typing import Optional
import streamlit as st

from naomi.agent import generate_llm_response, process_llm_response
from naomi.db import (
    DEFAULT_CONVERSATION_ID,
    MessageModel,
    add_message_to_db,
    delete_messages,
    fetch_messages,
    session_scope,
)
from utils import handle_login


def draw_chat():
    st.header("💬 Chat")

    with session_scope() as session:
        messages = fetch_messages(session, DEFAULT_CONVERSATION_ID)

        for message in messages:
            msg = message.content_dict
            with st.chat_message("user" if msg["role"] == "user" else "assistant"):
                if msg["role"] != "assistant":
                    col1, col2, _ = st.columns([1, 1, 2])
                    with col1:
                        st.write(message.id)
                    with col2:
                        if st.button("🗑️", key=f"delete_{message.id}"):
                            logging.info(f"Deleting message {message.id}")
                            delete_messages(session, DEFAULT_CONVERSATION_ID, message.id)
                            st.rerun()
                            return
                    st.markdown(msg["content"])
                else:
                    draw_assistant_message(message, session)

    if prompt := st.chat_input("Type your message here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        user_message = {"role": "user", "content": prompt}
        with session_scope() as session:
            add_message_to_db(user_message, session, DEFAULT_CONVERSATION_ID)

        with session_scope() as session:
            with st.chat_message("assistant"):
                draw_assistant_message(None, session)
                st.rerun()


def draw_assistant_message(existing_message: Optional[MessageModel], session):
    message_id = existing_message.id if existing_message else "draft"
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.write(message_id)

    with col2:
        if existing_message and st.button("🗑️", key=f"delete_{message_id}"):
            logging.info(f"Deleting message {existing_message.id}")
            delete_messages(session, DEFAULT_CONVERSATION_ID, existing_message.id)
            st.rerun()
            return

    with col3:
        regenerate = st.button("🔃 Regenerate", key=f"regenerate_{message_id}")

    if existing_message and not regenerate:
        st.markdown(existing_message.content_dict["content"])
        return

    if existing_message:
        delete_messages(session, DEFAULT_CONVERSATION_ID, existing_message.id)

    messages = [msg.content_dict for msg in fetch_messages(session, DEFAULT_CONVERSATION_ID)]
    response = generate_llm_response(messages)
    response_text = str(st.write_stream(process_llm_response(response)))
    if not existing_message:
        with st.spinner("Generating response..."):
            logging.debug(f"AI response: {response_text}")
            ai_message = {"role": "assistant", "content": response_text}
            existing_message = add_message_to_db(ai_message, session, DEFAULT_CONVERSATION_ID)
    else:
        with st.spinner("Regenerating response..."):
            msg = existing_message.content_dict
            msg["content"] = response_text
            add_message_to_db(msg, session, DEFAULT_CONVERSATION_ID)
    session.commit()
    st.rerun()


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    if not handle_login():
        exit(0)

    draw_chat()


if __name__ == "__main__":
    run()
