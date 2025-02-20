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
from typing import Iterator, Optional
import streamlit as st
from streamlit.logger import get_logger
from swarm import Agent  # type: ignore[import]

from naomi.db import DEFAULT_CONVERSATION_ID, MessageModel, add_message_to_db, session_scope
from llm.llm import handle_base_model_arg, llm_client
from llm.stream_processing import MessageStream, ToolStream, parse_streaming_response
from utils import handle_login

LOGGER = get_logger(__name__)


def generate_llm_response(model: Optional[str] = None) -> Iterator[str]:
    model = handle_base_model_arg(model)

    try:
        agent = Agent(
            name="Creative Assistant",
            model=model,
            instructions="You are a helpful assistant.",
            stream=True,
        )

        with session_scope() as session:
            messages = (
                session.query(MessageModel)
                .where(MessageModel.conversation_id == DEFAULT_CONVERSATION_ID)
                .order_by(MessageModel.id)
                .all()
            )
            message_contents = [msg.content_dict for msg in messages]

            chunks = llm_client().run(agent, message_contents, stream=True)
            for stream in parse_streaming_response(chunks):
                if isinstance(stream, MessageStream):
                    for chunk in stream.content_stream:
                        yield chunk
                elif isinstance(stream, ToolStream):
                    logging.debug(f"Tool Use: {stream}")
            logging.info("Response generation complete")
    except Exception as e:
        logging.error(f"Error generating response: {e}", exc_info=True)
        yield f"An error '{e}' occurred while generating the response. Please try again."


def draw_chat():
    st.header("💬 Chat")

    with session_scope() as session:
        messages = (
            session.query(MessageModel)
            .where(MessageModel.conversation_id == DEFAULT_CONVERSATION_ID)
            .order_by(MessageModel.id)
            .all()
        )

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
                            session.query(MessageModel).where(
                                MessageModel.conversation_id == DEFAULT_CONVERSATION_ID
                            ).where(MessageModel.id >= message.id).delete()
                            # session.query(SummaryModel).where(
                            #     SummaryModel.conversation_id == DEFAULT_CONVERSATION_ID
                            # ).where(
                            #     SummaryModel.summary_until_id >= message.id
                            # ).delete()
                            session.commit()
                            st.rerun()
                            return
                    st.markdown(msg["content"])
                else:
                    draw_assistant_message(message, session)

    if prompt := st.chat_input("Type your message here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
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
            session.query(MessageModel).where(
                MessageModel.conversation_id == DEFAULT_CONVERSATION_ID
            ).filter(MessageModel.id >= existing_message.id).delete()
            session.commit()
            st.rerun()
            return

    with col3:
        regenerate = st.button("🔃 Regenerate", key=f"regenerate_{message_id}")

    # conversation = draw_conversation_summary(session)
    # if not conversation:
    #     st.error("Summary required...")
    #     st.rerun()
    #     return

    if existing_message and not regenerate:
        st.markdown(existing_message.content_dict["content"])
        return

    if existing_message:
        session.query(MessageModel).where(
            MessageModel.conversation_id == DEFAULT_CONVERSATION_ID
        ).where(MessageModel.id >= existing_message.id).delete()
        # session.query(SummaryModel).where(
        #     SummaryModel.conversation_id == DEFAULT_CONVERSATION_ID
        # ).where(SummaryModel.summary_until_id >= existing_message.id).delete()
        session.commit()

    response = generate_llm_response()
    response_text = str(st.write_stream(response))
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
