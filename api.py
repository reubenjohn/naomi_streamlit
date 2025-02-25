from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from naomi_streamlit.db import WebhookEvent, initialize_db, session_scope


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield


app = FastAPI(
    root_path="/api",
    prefix="/api",
    lifespan=lifespan,
)


class WebhookEventRequest(BaseModel):
    type: str
    payload: Dict[str, Any]


@app.post("/webhook")
async def receive_webhook(event: WebhookEventRequest):
    with session_scope() as session:
        new_event = WebhookEvent(event_type=event.type, payload=str(event.payload))
        session.add(new_event)
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8090)
