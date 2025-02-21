from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from naomi.db import WebhookEvent, initialize_db, session_scope


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_db()
    yield


app = FastAPI(
    root_path="/api",
    prefix="/api",
    lifespan=lifespan,
)


@app.post("/api/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    event_type = data.get("type", "unknown")
    with session_scope() as session:
        new_event = WebhookEvent(event_type=event_type, payload=str(data))
        session.add(new_event)
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8090)
