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
from typing import Iterator, List, Optional
import streamlit as st
from streamlit.logger import get_logger
from swarm import Agent  # type: ignore[import]

from naomi.llm.llm import handle_base_model_arg, llm_client
from naomi.llm.stream_processing import MessageStream, ToolStream, parse_streaming_response
from utils import handle_login

LOGGER = get_logger(__name__)


def generate_brainstorm_response(
    instructions: str, messages: List[dict], model: Optional[str] = None
) -> Iterator[str]:
    model = handle_base_model_arg(model)

    try:
        agent = Agent(
            name="Creative Assistant",
            model=model,
            instructions=instructions,
            stream=True,
        )

        chunks = llm_client().run(agent, messages, stream=True)
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

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Clear chat"):
        st.session_state.messages = []

    def add_message(role, content):
        st.session_state.messages.append({"role": role, "content": content})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        add_message("user", prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(
                generate_brainstorm_response(
                    "You are a helpful assistant", st.session_state.messages
                )
            )
        add_message("assistant", response)

        st.rerun()


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    if not handle_login():
        exit(0)

    st.write("# Welcome to Streamlit! 👋")

    with st.sidebar:
        st.success("Select a demo above.")

    draw_chat()


if __name__ == "__main__":
    run()
