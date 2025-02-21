from naomi.db import MessageModel


class InstanceOf:
    """Custom matcher to check if a mock argument is an instance of a given class."""

    def __init__(self, cls):
        self.cls = cls

    def __eq__(self, other):
        return isinstance(other, self.cls)


def assert_message_model(actual: MessageModel, expected: MessageModel):
    assert actual.conversation_id == expected.conversation_id
    assert actual.id == expected.id
    assert actual.content == expected.content


def assert_message_persisted(expected: MessageModel, session):
    actual = session.query(MessageModel).filter_by(id=expected.id).one()
    assert actual.conversation_id == expected.conversation_id
    assert actual.id == expected.id
    assert actual.content == expected.content
