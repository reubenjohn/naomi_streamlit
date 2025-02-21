from contextlib import contextmanager
import os
from typing import Iterator
from unittest.mock import patch
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from naomi.db import (
    Base,
    Message,
    MessageModel,
)
from naomi.db import get_all_tables

os.environ["OPENAI_BASE_URL"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_BASE_MODEL"] = ""


TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def in_memory_session():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    InMemorySession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    yield InMemorySession()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def test_db():
    """Creates a new database for each test case."""

    with patch("naomi.db.engine", new_callable=lambda: engine):
        assert get_all_tables() == []

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

    with patch("naomi.db.engine", new_callable=lambda: engine):
        assert get_all_tables() == []


@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function", autouse=True)
def patched_session_scope(db_session):
    """Fixture to patch session_scope so it returns the test database session."""

    @contextmanager
    def mock_session_scope():
        yield db_session  # Return the test session

    with patch("naomi.db.session_scope", side_effect=mock_session_scope):
        yield  # Ensures patch is applied for the duration of the test


@pytest.fixture(scope="function")
def message_data() -> Message:
    return Message(content="Hello, NAOMI!")


@pytest.fixture(scope="function")
def message_data2() -> Message:
    return Message(content="How are you?")


@pytest.fixture(scope="function")
def message1(message_data):
    return MessageModel(conversation_id=1, id=1, content=message_data.to_json())


@pytest.fixture(scope="function")
def message2(message_data2):
    return MessageModel(conversation_id=1, id=2, content=message_data2.to_json())


@pytest.fixture(scope="function")
def persist_messages(db_session, message1: MessageModel, message2: MessageModel):
    db_session.add(message1)
    db_session.add(message2)
    db_session.commit()
    return message1, message2


@pytest.fixture
def mock_llm_client():
    with patch("naomi.assistant.agent.llm_client") as mock:
        yield mock


def pass_thru_process_llm_response(chunks: Iterator[str]) -> Iterator[str]:
    return chunks


@pytest.fixture(scope="function", autouse=True)
def patch_process_llm_response():
    with patch(
        "naomi.assistant.persistence.process_llm_response",
        side_effect=pass_thru_process_llm_response,
    ):
        yield
