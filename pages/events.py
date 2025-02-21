import streamlit as st
from naomi.db import WebhookEvent, session_scope


def event_form():
    with st.form("event_form"):
        event_type = st.text_input("Event Type", value="email")
        payload = st.text_area(
            "Payload",
            """{
    "subject": "PNC Statement",
    "body": "..."
    }""",
        )
        st.json(payload)
        if st.form_submit_button("Submit"):
            with session_scope() as session:
                new_event = WebhookEvent(event_type=event_type, payload=payload)
                session.add(new_event)
            st.success("Event added successfully!")


def show_events():
    st.title("Event Logger")

    with st.expander("Add Event", expanded=True):
        event_form()

    if st.button("Refresh"):
        st.rerun()

    with session_scope() as session:
        events = session.query(WebhookEvent).order_by(WebhookEvent.created_at.asc()).all()
        st.table(
            [
                {
                    "ID": e.id,
                    "Type": e.event_type,
                    "Payload": e.payload,
                    "Created": e.created_at,
                    "Status": e.status,
                }
                for e in events
            ]
        )


show_events()
