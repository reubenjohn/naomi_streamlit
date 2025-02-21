from streamlit.testing.v1 import AppTest
from unittest.mock import patch


def handle_login_wrapper():  # pragma: no cover
    import streamlit as st
    from naomi.utils import handle_login

    st.session_state["_is_logged_in_"] = handle_login()


@patch("naomi.utils.st.experimental_user")
def test_handle_login_logged_in(mock_experimental_user):
    mock_experimental_user.get.return_value = True
    mock_experimental_user.name = "Test User"

    at = AppTest.from_function(handle_login_wrapper)
    at.run()

    assert not at.exception
    assert 1 == len(at.sidebar.markdown)
    assert "Hello, Test User!" == at.sidebar.markdown[0].value
    assert 1 == len(at.sidebar.button)
    assert at.sidebar.button[0].label == "Log out"
    assert at.session_state["_is_logged_in_"] is True


@patch("naomi.utils.st.experimental_user")
def test_handle_login_not_logged_in(mock_experimental_user):
    mock_experimental_user.get.return_value = False

    at = AppTest.from_function(handle_login_wrapper)
    at.run()

    assert not at.exception
    assert 1 == len(at.sidebar.error)
    assert "You need to log in to continue." == at.sidebar.error[0].value
    assert 1 == len(at.sidebar.button)
    assert at.sidebar.button[0].label == "Log in"


@patch("naomi.utils.st.experimental_user")
@patch("naomi.utils.st.logout")
def test_handle_logout_button(mock_logout, mock_experimental_user):
    mock_experimental_user.get.return_value = True
    mock_experimental_user.name = "Test User"

    at = AppTest.from_function(handle_login_wrapper)
    at.run()

    assert not at.exception
    assert 1 == len(at.sidebar.button)
    assert at.sidebar.button[0].label == "Log out"

    at.sidebar.button[0].click().run()

    assert not at.exception
    mock_logout.assert_called_once()


@patch("naomi.utils.st.experimental_user")
@patch("naomi.utils.st.login")
def test_handle_login_button(mock_login, mock_experimental_user):
    mock_experimental_user.get.return_value = False

    at = AppTest.from_function(handle_login_wrapper)
    at.run()

    assert not at.exception
    assert 1 == len(at.sidebar.button)
    assert at.sidebar.button[0].label == "Log in"

    at.sidebar.button[0].click().run()

    assert not at.exception
    mock_login.assert_called_once()
