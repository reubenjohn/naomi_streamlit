import pytest
from streamlit.testing.v1 import AppTest
from unittest.mock import patch


def run_wrapper():  # pragma: no cover
    import streamlit as st
    from naomi.home import run

    try:
        run()
        st.session_state["_exit_code_"] = None
    except SystemExit as e:
        st.session_state["_exit_code_"] = e.code


@patch("naomi.home.handle_login")
@patch("naomi.home.draw_chat")
def test_run_logged_in(mock_draw_chat, mock_handle_login):
    mock_handle_login.return_value = True

    at = AppTest.from_function(run_wrapper)
    at.run()

    assert not at.exception
    assert mock_handle_login.called
    assert mock_draw_chat.called

    assert at.session_state["_exit_code_"] is None


@patch("naomi.home.handle_login")
@patch("naomi.home.draw_chat")
def test_run_not_logged_in(mock_draw_chat, mock_handle_login):
    mock_handle_login.return_value = False

    at = AppTest.from_function(run_wrapper)
    at.run()

    assert not at.exception
    assert mock_handle_login.called
    assert not mock_draw_chat.called

    assert at.session_state["_exit_code_"] == 0
