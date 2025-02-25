import pytest
from naomi_streamlit.db import MessageModel
from tests.conftest import in_memory_session
from tests.matchers import (
    InstanceOf,
    EqualsMessageModel,
    EqualsMessageModels,
    assert_message_model,
    assert_message_persisted,
)


def test_instance_of():
    assert InstanceOf(int) == 42
    assert not (InstanceOf(int) == "not an int")


def test_equals_message_model():
    message1 = MessageModel(conversation_id=1, id=1, content="Hello!")
    message2 = MessageModel(conversation_id=1, id=1, content="Hello!")
    message3 = MessageModel(conversation_id=1, id=2, content="Hello!")
    message4 = MessageModel(conversation_id=1, id=1, content="Hi!")

    assert EqualsMessageModel(message1) == message2
    assert not (EqualsMessageModel(message1) == message3)
    assert not (EqualsMessageModel(message1) == message4)
    assert not (EqualsMessageModel(message1) == "not a message model")


def test_equals_message_models():
    messages1 = [
        MessageModel(conversation_id=1, id=1, content="Hello!"),
        MessageModel(conversation_id=1, id=2, content="Hi!"),
    ]
    messages2 = [
        MessageModel(conversation_id=1, id=1, content="Hello!"),
        MessageModel(conversation_id=1, id=2, content="Hi!"),
    ]
    messages3 = [
        MessageModel(conversation_id=1, id=1, content="Hello!"),
        MessageModel(conversation_id=1, id=3, content="Hi!"),
    ]
    messages4 = [
        MessageModel(conversation_id=1, id=1, content="Hello!"),
        MessageModel(conversation_id=1, id=2, content="Hello!"),
    ]

    assert EqualsMessageModels(messages1) == messages2
    assert not (EqualsMessageModels(messages1) == messages3)
    assert not (EqualsMessageModels(messages1) == messages4)
    assert not (EqualsMessageModels(messages1) == "not a list of message models")


def test_assert_message_model():
    message1 = MessageModel(conversation_id=1, id=1, content="Hello!")
    message2 = MessageModel(conversation_id=1, id=1, content="Hello!")
    message3 = MessageModel(conversation_id=1, id=2, content="Hello!")
    message4 = MessageModel(conversation_id=1, id=2, content="Hi!")

    assert_message_model(message1, message2)

    with pytest.raises(AssertionError):
        assert_message_model(message1, message3)

    with pytest.raises(AssertionError):
        assert_message_model(message1, message4)


def test_assert_message_persisted():
    message = MessageModel(conversation_id=1, id=1, content="Hello!")

    with in_memory_session() as session:
        session.add(message)
        session.commit()
        assert_message_persisted(message, session)

    with in_memory_session() as session:
        with pytest.raises(AssertionError):
            assert_message_persisted(MessageModel(conversation_id=1, id=2, content="Hi!"), session)
