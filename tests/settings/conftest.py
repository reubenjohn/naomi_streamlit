import pytest
from naomi_core.db.agent import AgentModel, AgentResponsibilityModel


def run_wrapper():  # pragma: no cover
    import streamlit as st
    from naomi_streamlit.settings.settings_tabs import show_settings

    try:
        show_settings()
        st.session_state["_exit_code_"] = None
    except SystemExit as e:
        st.session_state["_exit_code_"] = e.code


@pytest.fixture
def mock_agent():
    return AgentModel(name="Test Agent", prompt="Test prompt")


@pytest.fixture
def mock_responsibility():
    return AgentResponsibilityModel(
        agent_name="Test Agent",
        name="Test Responsibility",
        description="Test description",
    )
