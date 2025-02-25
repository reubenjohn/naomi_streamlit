import streamlit as st
from naomi_streamlit.db import WebhookEvent, session_scope


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
        for event in events:
            cols = st.columns([0.5, 2, 2, 1, 1])
            cols[0].write(event.id)
            cols[1].write(event.event_type)
            cols[2].write(event.created_at)
            cols[3].write(event.status)
            if cols[4].button("🗑️", key=f"delete_{event.id}"):
                with session_scope() as delete_session:
                    delete_event = delete_session.query(WebhookEvent).get(event.id)
                    delete_session.delete(delete_event)
                    st.success(f"Event {event.id} deleted successfully!")
                st.rerun()
            with st.expander("Payload", expanded=False):
                st.json(event.payload)
            st.divider()


show_events()
