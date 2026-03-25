from __future__ import annotations

import os
import uuid

from fastapi import APIRouter
from pydantic import BaseModel

from core.shared.config import settings

router = APIRouter(tags=["chat"])

# In-memory session store (per server process)
_sessions: dict[str, list[dict[str, str]]] = {}


class ChatRequest(BaseModel):
    message: str
    model: str = ""
    system: str = "You are a helpful AI assistant."
    session_id: str = ""


class ChatResponse(BaseModel):
    reply: str
    model: str
    session_id: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    model = req.model or settings.default_model
    api_key = os.environ.get("GEMINI_API_KEY", "") or os.environ.get("GOOGLE_API_KEY", "") or settings.google_api_key
    session_id = req.session_id or str(uuid.uuid4())

    if not api_key:
        return ChatResponse(
            reply="[Mock] No GOOGLE_API_KEY found in env or .env. Your message was: " + req.message,
            model="mock",
            session_id=session_id,
        )

    # Build conversation history
    if session_id not in _sessions:
        _sessions[session_id] = []

    _sessions[session_id].append({"role": "user", "parts": [{"text": req.message}]})

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    import time
    start = time.monotonic()
    response = client.models.generate_content(
        model=model,
        contents=_sessions[session_id],
        config=types.GenerateContentConfig(
            system_instruction=req.system,
        ),
    )
    elapsed = (time.monotonic() - start) * 1000

    reply_text = response.text or ""

    # Save assistant reply to history
    _sessions[session_id].append({"role": "model", "parts": [{"text": reply_text}]})

    # Keep history manageable (last 40 turns)
    if len(_sessions[session_id]) > 40:
        _sessions[session_id] = _sessions[session_id][-40:]

    return ChatResponse(
        reply=reply_text,
        model=model,
        session_id=session_id,
        input_tokens=getattr(response.usage_metadata, "prompt_token_count", 0) if response.usage_metadata else 0,
        output_tokens=getattr(response.usage_metadata, "candidates_token_count", 0) if response.usage_metadata else 0,
        latency_ms=elapsed,
    )
