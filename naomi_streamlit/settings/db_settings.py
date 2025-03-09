import streamlit as st

from naomi_core.db.core import get_all_tables, wipe_db


def show_database_tab():
    if st.button("💀 Wipe database", key="wipe_db"):
        wipe_db()
        st.success("Database wiped")
        st.rerun()
    st.subheader("Tables")
    st.table(get_all_tables())
