from fastapi import FastAPI
from pydantic import BaseModel

import config

# EXISTING IMPORTS
from brain.llm import chat
from memory.store import add_message, get_messages

# NEW IMPORTS (auth + database)
from database.init_db import init_db
from routers.api_keys import router as api_keys_router
from middleware.usage_tracking import UsageTrackingMiddleware

# CREATE APP
app = FastAPI(title="Coreyt Enterprise API")

# INITIALIZE DATABASE ON STARTUP
@app.on_event("startup")
def startup():
    init_db()

# ADD USAGE TRACKING MIDDLEWARE
app.add_middleware(UsageTrackingMiddleware)

# REGISTER API KEY ROUTES
app.include_router(api_keys_router)


# =========================
# EXISTING MODELS
# =========================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    user_id: str
    messages: list[Message]


# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def home():
    return {"status": "Coreyt Enterprise Running"}


# =========================
# CHAT ENDPOINT
# =========================

@app.post("/v1/chat/completions")
def chat_completions(request: ChatRequest):

    user_id = request.user_id

    history = get_messages(user_id)

    new_messages = [m.dict() for m in request.messages]

    full_conversation = history + new_messages

    response = chat(full_conversation)

    for m in new_messages:
        add_message(user_id, m["role"], m["content"])

    add_message(user_id, "assistant", response)

    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response
                }
            }
        ]
    }