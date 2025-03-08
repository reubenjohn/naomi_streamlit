from streamlit.testing.v1 import AppTest


def show_llm_response_wrapper():  # pragma: no cover
    from naomi_streamlit.chat.assistant import show_llm_response

    chunks = iter(["chunk1", "chunk2", "chunk3"])
    return show_llm_response(chunks, "Test Spinner")


def show_llm_generation_wrapper():  # pragma: no cover
    from naomi_streamlit.chat.assistant import show_llm_generation

    chunks = iter(["chunk1", "chunk2", "chunk3"])
    return show_llm_generation(chunks)


def show_llm_regeneration_wrapper():  # pragma: no cover
    from naomi_streamlit.chat.assistant import show_llm_regeneration

    chunks = iter(["chunk1", "chunk2", "chunk3"])
    return show_llm_regeneration(chunks)


def draw_assistant_message_wrapper():  # pragma: no cover
    from naomi_streamlit.chat.assistant import draw_assistant_message
    from naomi_core.db.chat import MessageModel, Message
    from tests.conftest import in_memory_session
    import streamlit as st

    with in_memory_session() as session:
        draw_assistant_message(
            MessageModel(
                conversation_id=1, id=1, content=Message.from_user_input("Hello!").to_json()
            ),
            session,
        )
        st.session_state["_message_count_"] = session.query(MessageModel).count()


def draw_draft_assistant_message_wrapper():  # pragma: no cover
    from naomi_streamlit.chat.assistant import draw_draft_assistant_message
    from tests.conftest import in_memory_session

    with in_memory_session() as session:
        draw_draft_assistant_message(1, session)


def test_show_llm_response():
    at = AppTest.from_function(show_llm_response_wrapper)
    at.run()

    assert not at.exception
    assert "chunk1chunk2chunk3" in at.markdown[0].value


def test_show_llm_generation():
    at = AppTest.from_function(show_llm_generation_wrapper)
    at.run()

    assert not at.exception
    assert "chunk1chunk2chunk3" in at.markdown[0].value


def test_show_llm_regeneration():
    at = AppTest.from_function(show_llm_regeneration_wrapper)
    at.run()

    assert not at.exception
    assert "chunk1chunk2chunk3" in at.markdown[0].value


def test_draw_assistant_message():
    at = AppTest.from_function(draw_assistant_message_wrapper)
    at.run()

    assert not at.exception
    assert 0 == at.session_state["_message_count_"]

    assert len(at.markdown) == 2
    assert at.markdown[0].value
    assert "`1`" in at.markdown[0].value
    assert "Hello!" in at.markdown[1].value

    assert len(at.button) == 2
    assert at.button[0].key == "regenerate_1"
    assert at.button[0].label == "🔃"
    assert at.button[1].key == "delete_1"
    assert at.button[1].label == "🗑️"


def test_draw_assistant_message_regenerate_button(mock_llm_client):
    at = AppTest.from_function(draw_assistant_message_wrapper)
    at.run()
    assert not at.exception
    assert 0 == at.session_state["_message_count_"]

    assert "Hello!" in at.markdown[1].value

    mock_llm_client.return_value.run.return_value = iter(["Regenerated"])
    at.button[0].click().run()
    assert not at.exception
    assert 1 == at.session_state["_message_count_"]

    assert len(at.markdown) == 2
    assert at.markdown[0].value
    assert "`1`" in at.markdown[0].value
    assert "Regenerated" in at.markdown[1].value

    assert len(at.button) == 2
    assert at.button[0].key == "regenerate_1"
    assert at.button[0].label == "🔃"
    assert at.button[1].key == "delete_1"
    assert at.button[1].label == "🗑️"


def test_draw_assistant_message_delete_button():
    at = AppTest.from_function(draw_assistant_message_wrapper)
    at.run()

    assert not at.exception
    assert 0 == at.session_state["_message_count_"]

    assert len(at.markdown) == 2

    at.button[1].click().run()

    assert not at.exception

    assert len(at.markdown) == 2
    assert at.markdown[0].value
    assert "`1`" in at.markdown[0].value
    assert "Hello!" in at.markdown[1].value

    assert len(at.button) == 2
    assert at.button[0].key == "regenerate_1"
    assert at.button[0].label == "🔃"
    assert at.button[1].key == "delete_1"
    assert at.button[1].label == "🗑️"


def test_draw_draft_assistant_message_regenerate_button(mock_llm_client):
    mock_llm_client.return_value.run.return_value = iter(["Generated"])
    at = AppTest.from_function(draw_draft_assistant_message_wrapper)
    at.run()
    assert not at.exception

    assert len(at.markdown) == 2
    assert at.markdown[0].value
    assert "draft" in at.markdown[0].value
    assert "Generated" in at.markdown[1].value
