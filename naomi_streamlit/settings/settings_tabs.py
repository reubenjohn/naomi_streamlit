import streamlit as st

from naomi_streamlit.settings.agent_settings import show_agents_tab
from naomi_streamlit.settings.db_settings import show_database_tab


def show_settings():
    st.set_page_config(
        page_title="NAOMI Settings",
        page_icon="⚙️",
    )
    st.title("Settings")

    if st.button("🔄 Refresh", key="refresh"):
        st.rerun()

    (agents_tab, db_tab) = st.tabs(["🤖 Agents", "💿 Database"])

    with db_tab:
        show_database_tab()

    with agents_tab:
        show_agents_tab()
