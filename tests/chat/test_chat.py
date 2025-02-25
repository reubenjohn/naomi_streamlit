from streamlit.testing.v1 import AppTest
from unittest.mock import MagicMock, patch

from naomi_streamlit.db import DEFAULT_CONVERSATION_ID, Message
from tests.matchers import EqualsMessageModel, InstanceOf
from tests.data import message_model_1, message_model_2, message_model_3


def draw_messages_wrapper():  # pragma: no cover
    from naomi_streamlit.chat.chat import draw_messages
    from tests.data import message_model_1, message_model_2
    from unittest.mock import MagicMock

    messages = [message_model_1(), message_model_2()]
    draw_messages(messages, MagicMock())


@patch("naomi_streamlit.chat.chat.draw_assistant_message")
@patch("naomi_streamlit.chat.chat.draw_user_message")
def test_draw_messages(mock_draw_user_message, mock_draw_assistant_message):
    at = AppTest.from_function(draw_messages_wrapper)
    at.run()

    assert not at.exception

    assert at.main.children[0].type == "chat_message"
    assert at.main.children[0].avatar == "user"
    assert at.main.children[1].type == "chat_message"
    assert at.main.children[1].avatar == "assistant"

    mock_draw_user_message.assert_called_once_with(
        EqualsMessageModel(message_model_1()), InstanceOf(MagicMock)
    )
    mock_draw_assistant_message.assert_called_once_with(
        EqualsMessageModel(message_model_2()), InstanceOf(MagicMock)
    )


def draw_chat_wrapper():  # pragma: no cover
    from naomi_streamlit.chat.chat import draw_chat

    draw_chat()


@patch("naomi_streamlit.chat.chat.session_scope")
@patch("naomi_streamlit.chat.chat.fetch_messages")
@patch("naomi_streamlit.chat.chat.add_message_to_db")
@patch("naomi_streamlit.chat.chat.draw_draft_assistant_message")
@patch("naomi_streamlit.chat.chat.draw_assistant_message")
@patch("naomi_streamlit.chat.chat.draw_user_message")
def test_draw_chat(
    mock_draw_user_message,
    mock_draw_assistant_message,
    mock_draw_draft_assistant_message,
    mock_add_message_to_db,
    mock_fetch_messages,
    mock_session_scope,
):
    mock_session_scope.return_value.__enter__.return_value = None
    mock_fetch_messages.return_value = [message_model_1(), message_model_2()]

    at = AppTest.from_function(draw_chat_wrapper)
    at.run()

    assert not at.exception

    assert at.main.children[0].type == "header"
    assert "💬 Chat" in at.main.children[0].value
    assert at.main.children[1].type == "chat_message"
    assert at.main.children[1].avatar == "user"
    assert at.main.children[2].type == "chat_message"
    assert at.main.children[2].avatar == "assistant"

    assert mock_draw_user_message.call_count == 1
    assert mock_draw_assistant_message.call_count == 1

    assert not mock_add_message_to_db.called
    assert not mock_draw_draft_assistant_message.called


@patch("naomi_streamlit.chat.chat.session_scope")
@patch("naomi_streamlit.chat.chat.fetch_messages")
@patch("naomi_streamlit.chat.chat.add_message_to_db")
@patch("naomi_streamlit.chat.chat.draw_draft_assistant_message")
@patch("naomi_streamlit.chat.chat.draw_assistant_message")
@patch("naomi_streamlit.chat.chat.draw_user_message")
def test_draw_chat_user_input(
    mock_draw_user_message,
    mock_draw_assistant_message,
    mock_draw_draft_assistant_message,
    mock_add_message_to_db,
    mock_fetch_messages,
    mock_session_scope,
):
    mock_session_scope.return_value.__enter__.return_value = None
    mock_fetch_messages.return_value = [message_model_1(), message_model_2()]

    def on_add_user_message(message: Message, conversation_id, _):
        assert message["content"] == "Do you know any jokes?"
        assert conversation_id == DEFAULT_CONVERSATION_ID
        mock_fetch_messages.return_value = [message_model_1(), message_model_2(), message_model_3()]

    mock_add_message_to_db.side_effect = on_add_user_message

    at = AppTest.from_function(draw_chat_wrapper)
    at.run()

    assert mock_draw_user_message.call_count == 1
    assert mock_draw_assistant_message.call_count == 1

    assert not at.exception

    at.chat_input[0].set_value("Do you know any jokes?").run()

    assert not at.exception

    assert "💬 Chat" in at.main.children[0].value
    assert at.main.children[1].type == "chat_message"
    assert at.main.children[1].avatar == "user"
    assert at.main.children[2].type == "chat_message"
    assert at.main.children[2].avatar == "assistant"

    assert len(at.markdown) == 1
    assert "Do you know any jokes?" in at.markdown[0].value

    # 1 initial call, then +1 when button is clicked and +2 after add_message_to_db is called
    assert mock_draw_user_message.call_count == 4
    assert mock_draw_assistant_message.call_count == 3

    mock_add_message_to_db.assert_called_once()
    mock_draw_draft_assistant_message.assert_called_once()
