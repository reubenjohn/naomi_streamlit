from streamlit.testing.v1 import AppTest


def draw_user_message_wrapper():  # pragma: no cover
    from naomi_streamlit.chat.user_input import draw_user_message
    from naomi_core.db import MessageModel
    from naomi_core.db import Message
    from tests.conftest import in_memory_session

    with in_memory_session() as session:
        draw_user_message(
            MessageModel(conversation_id=1, id=1, content=Message(content="Hello!").to_json()),
            session,
        )


def test_draw_user_message():
    at = AppTest.from_function(draw_user_message_wrapper)
    at.run()

    assert not at.exception

    assert len(at.markdown) == 2
    assert at.markdown[0].value
    assert "`1`" in at.markdown[0].value
    assert "Hello!" in at.markdown[1].value
    assert len(at.button) == 1
    assert at.button[0].key == "delete_1"
    assert at.button[0].label == "🗑️"


def test_draw_user_message_button_press():
    at = AppTest.from_function(draw_user_message_wrapper)
    at.run()

    at.button[0].click().run()

    assert not at.exception

    assert len(at.markdown) == 2
    assert at.markdown[0].value
    assert "`1`" in at.markdown[0].value
    assert "Hello!" in at.markdown[1].value
    assert len(at.button) == 1
    assert at.button[0].key == "delete_1"
    assert at.button[0].label == "🗑️"
