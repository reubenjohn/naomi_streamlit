from contextlib import contextmanager
import json
from unittest.mock import patch
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from naomi.db import (
    Base,
    MessageModel,
    delete_messages,
    fetch_messages,
    initialize_db,
    save_agent_goal,
    add_message_to_db,
    AgentGoalModel,
    load_goals_from_db,
    session_scope,
)
from naomi.db import Conversation, SummaryModel, PropertyModel, get_all_tables

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
def message_data():
    return {"content": "Hello, NAOMI!"}


@pytest.fixture(scope="function")
def message_data2():
    return {"content": "How are you?"}


@pytest.fixture(scope="function")
def create_messages(db_session, message_data, message_data2):
    message1 = MessageModel(conversation_id=1, id=1, content=json.dumps(message_data))
    message2 = MessageModel(conversation_id=1, id=2, content=json.dumps(message_data2))
    db_session.add(message1)
    db_session.add(message2)
    db_session.commit()
    return message1, message2


@patch("naomi.db.engine", new_callable=lambda: engine)
def test_initialize_db_and_get_all_tables(_):
    Base.metadata.drop_all(bind=engine)
    assert [] == get_all_tables()
    initialize_db()
    assert {"conversation", "message", "summary", "agent_goal", "property"} == {
        t[0] for t in get_all_tables()
    }


def test_add_message(db_session, message_data):
    result = add_message_to_db(message_data, db_session, conversation_id=1)
    db_session.commit()
    assert result.id == 1
    assert result.content_dict == message_data
    saved_message = db_session.query(MessageModel).filter_by(id=1).one()
    assert saved_message.content_dict == message_data


def test_message_content_functions(db_session, message_data):
    message = MessageModel(conversation_id=1, id=1, content=json.dumps(message_data))
    db_session.add(message)
    db_session.commit()
    saved_message = db_session.query(MessageModel).filter_by(id=1).one()
    assert saved_message.content_dict == message_data
    assert saved_message.content_dumps == json.dumps(message_data)
    assert saved_message.content_val == "Hello, NAOMI!"


def test_fetch_messages(db_session, create_messages, message_data, message_data2):
    messages = fetch_messages(db_session, conversation_id=1)
    assert len(messages) == 2
    assert messages[0].content_dict == message_data
    assert messages[1].content_dict == message_data2


def test_delete_messages(db_session, create_messages, message_data):
    delete_messages(db_session, conversation_id=1, message_id=2)
    messages = fetch_messages(db_session, conversation_id=1)
    assert len(messages) == 1
    assert messages[0].content_dict == message_data


def test_save_and_load_agent_goal(db_session):
    new_goal = AgentGoalModel(
        name="SaveGoal", description="Testing save", completed=False, persistence="temp"
    )
    save_agent_goal(new_goal)
    db_session.commit()
    goals = load_goals_from_db()
    assert [g.name for g in goals] == ["SaveGoal"]

    goal = AgentGoalModel(name="TestGoal", description="Test", completed=False, persistence="temp")
    db_session.add(goal)
    db_session.commit()
    goals = load_goals_from_db()
    assert any(g.name == "TestGoal" for g in goals)


def test_create_and_query_models(db_session):
    convo = Conversation(name="TestConvo", description="A test conversation")
    db_session.add(convo)
    summary = SummaryModel(conversation_id=42, summary_until_id=1, content="Summarized content")
    db_session.add(summary)
    prop = PropertyModel(key="testKey", value="testValue")
    db_session.add(prop)
    db_session.commit()

    saved_convo = db_session.query(Conversation).filter_by(name="TestConvo").one()
    assert saved_convo.description == "A test conversation"
    saved_summary = db_session.query(SummaryModel).filter_by(conversation_id=42).one()
    assert saved_summary.content == "Summarized content"
    saved_prop = db_session.query(PropertyModel).filter_by(key="testKey").one()
    assert saved_prop.value == "testValue"


@patch("naomi.db.Session", new_callable=lambda: TestingSessionLocal)
def test_session_scope(mock_session):
    with session_scope() as session:
        assert session is not None
        assert isinstance(session, type(mock_session()))
        # Perform some operations to ensure session is working
        convo = Conversation(name="TestConvo", description="A test conversation")
        session.add(convo)
        session.commit()
        saved_convo = session.query(Conversation).filter_by(name="TestConvo").one()
        assert saved_convo.description == "A test conversation"


@patch("naomi.db.Session", new_callable=lambda: TestingSessionLocal)
def test_session_scope_commit(mock_session, db_session):
    with session_scope() as session:
        assert session is not None
        assert isinstance(session, type(mock_session()))
        convo = Conversation(name="TestConvo", description="A test conversation")
        session.add(convo)
    saved_convo = db_session.query(Conversation).filter_by(name="TestConvo").one()
    assert saved_convo.description == "A test conversation"


@patch("naomi.db.Session", new_callable=lambda: TestingSessionLocal)
def test_session_scope_rollback(mock_session):
    try:
        with session_scope() as session:
            assert session is not None
            assert isinstance(session, type(mock_session()))
            convo = Conversation(name="TestConvo", description="A test conversation")
            session.add(convo)
            raise Exception("Force rollback")
    except Exception:
        pass
    # assert session.is_active is False  # Ensure session is closed
    with session_scope() as session:
        saved_convo = session.query(Conversation).filter_by(name="TestConvo").first()
        assert saved_convo is None  # Ensure rollback occurred
