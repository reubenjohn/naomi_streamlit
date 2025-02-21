from streamlit.testing.v1 import AppTest


def draw_assistant_message_wrapper():  # pragma: no cover
    from naomi.chat.assistant import draw_assistant_message
    from naomi.db import MessageModel
    from tests.conftest import in_memory_session

    with in_memory_session() as session:
        draw_assistant_message(
            MessageModel(conversation_id=1, id=1, payload={"body": "Hello!"}),
            session,
        )


def draw_draft_assistant_message_wrapper():  # pragma: no cover
    from naomi.chat.assistant import draw_draft_assistant_message
    from tests.conftest import in_memory_session

    with in_memory_session() as session:
        draw_draft_assistant_message(1, session)


def show_llm_response_wrapper():  # pragma: no cover
    from naomi.chat.assistant import show_llm_response

    chunks = iter(["chunk1", "chunk2", "chunk3"])
    return show_llm_response(chunks, "Test Spinner")


def show_llm_generation_wrapper():  # pragma: no cover
    from naomi.chat.assistant import show_llm_generation

    chunks = iter(["chunk1", "chunk2", "chunk3"])
    return show_llm_generation(chunks)


def show_llm_regeneration_wrapper():  # pragma: no cover
    from naomi.chat.assistant import show_llm_regeneration

    chunks = iter(["chunk1", "chunk2", "chunk3"])
    return show_llm_regeneration(chunks)


# def test_draw_assistant_message():
#     at = AppTest.from_function(draw_assistant_message_wrapper)
#     at.run()

#     assert not at.exception

#     assert len(at.markdown) == 1
#     assert "Hello!" in at.markdown[0].value
#     assert len(at.button) == 2
#     assert at.button[0].key == "delete_1"
#     assert at.button[0].label == "🗑️"
#     assert at.button[1].key == "regenerate_1"
#     assert at.button[1].label == "🔃"


# def test_draw_assistant_message_button_press():
#     at = AppTest.from_function(draw_assistant_message_wrapper)
#     at.run()

#     at.button[0].click().run()

#     assert not at.exception

#     assert len(at.markdown) == 0
#     assert len(at.button) == 0


# def test_draw_draft_assistant_message():
#     at = AppTest.from_function(draw_draft_assistant_message_wrapper)
#     at.run()

#     assert not at.exception

#     assert len(at.markdown) == 1
#     assert "draft" in at.markdown[0].value


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
