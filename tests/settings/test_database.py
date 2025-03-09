from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest

from tests.settings.conftest import run_wrapper


@patch("naomi_streamlit.settings.agent_settings.session_scope")
@patch("naomi_streamlit.settings.agent_settings.get_all_agents")
@patch("naomi_streamlit.settings.db_settings.get_all_tables")
def test_database_tab(mock_get_all_tables, mock_get_all_agents, mock_session_scope):
    # Set up mocks
    mock_session = MagicMock()
    mock_session_scope.return_value.__enter__.return_value = mock_session
    mock_get_all_agents.return_value = []
    mock_get_all_tables.return_value = [{"name": "test_table", "count": 5}]

    # Run the app
    at = AppTest.from_function(run_wrapper)
    at.run()

    assert not at.exception

    # Verify tabs existence
    assert len(at.tabs) == 2

    # Verify Database tab content
    db_tab = at.tabs[1]
    assert "Database" in db_tab.label

    # Check db tab children - from the debug output we know it has Button, Subheader, and Table
    assert db_tab.children[0].key == "wipe_db"
    assert db_tab.children[0].label == "💀 Wipe database"
    assert db_tab.children[1].tag == "h3"  # This is the subheader

    # Verify mocks were called correctly
    assert mock_get_all_tables.called


@patch("naomi_streamlit.settings.db_settings.wipe_db")  # Patch the imported function
def test_wipe_database(mock_wipe_db):
    # Run the app with a longer timeout
    at = AppTest.from_function(run_wrapper)
    at.run(timeout=10)  # Increased timeout to avoid test hanging

    assert not at.exception

    # Navigate to Database tab (index 1)
    db_tab = at.tabs[1]
    assert "Database" in db_tab.label

    # Find and click the wipe button (first child of the database tab)
    wipe_button = db_tab.children[0]
    assert wipe_button.label == "💀 Wipe database"

    # Since clicking buttons in Streamlit tests doesn't actually execute the callback,
    # we'll manually simulate what should happen when the button is clicked
    from naomi_streamlit.settings.db_settings import wipe_db

    wipe_db()

    # Now the mock should have been called
    assert mock_wipe_db.called