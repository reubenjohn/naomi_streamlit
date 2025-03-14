import streamlit as st

from naomi_core.db.agent import (
    AgentModel,
    AgentResponsibilityModel,
    get_all_agents,
    load_responsibilities_from_db,
)
from naomi_core.db.core import session_scope


def agent_settings_form(agent: AgentModel, session):
    st.header(f"{agent.name} Agent")
    if st.button("🗑️ Delete", key=f"{agent.name}_delete"):
        session.delete(agent)
        st.success(f"{agent.name} Agent deleted")
        st.rerun()
    with st.form(key=f"{agent.name}_agent_settings"):
        lead_agent_prompt = st.text_area("Prompt", value=agent.prompt)
        if st.form_submit_button("Save"):
            agent.prompt = lead_agent_prompt  # type: ignore
            session.add(agent)
            st.success(f"{agent.name} Agent settings saved")

    responsibilities = load_responsibilities_from_db(agent, session)
    st.subheader(f"Responsibilities ({len(responsibilities)})")
    new_responsibility_form(agent, session)
    for responsibility in responsibilities:
        responsibility_form(responsibility, session)


def new_responsibility_form(agent: AgentModel, session):
    with st.expander("➕ Create New Responsibility"):
        with st.form(key=f"{agent.name}_new_responsibility", clear_on_submit=True, border=False):
            name = st.text_input("Name")
            description = st.text_area("Description")
            if st.form_submit_button("➕Create"):
                responsibility = AgentResponsibilityModel(
                    name=name,
                    agent_name=agent.name,
                    description=description,
                )
                session.add(responsibility)
                st.success(f"{responsibility.name} Responsibility created")
                return responsibility


def responsibility_form(responsibility: AgentResponsibilityModel, session):
    with st.expander(str(responsibility.name), expanded=False):
        with st.form(
            key=f"{responsibility.name}_responsibility_settings", clear_on_submit=True, border=False
        ):
            description = st.text_area("Description", value=responsibility.description)
            if st.form_submit_button("Save"):
                responsibility.description = description  # type: ignore
                session.add(responsibility)
                st.success(f"{responsibility.name} Responsibility saved")
        if st.button("🗑️ Delete", key=f"{responsibility.agent_name}_{responsibility.name}_delete"):
            session.delete(responsibility)
            session.commit()
            st.success(f"'{responsibility.name}' Responsibility deleted")
            st.rerun()


def show_agents_tab():
    with session_scope() as session:
        for agent in get_all_agents(session):
            agent_settings_form(agent, session)
            st.divider()
