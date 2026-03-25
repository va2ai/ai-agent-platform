from __future__ import annotations

from typing import Any


class SessionMemory:
    """In-memory conversation/task state for the current session."""

    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, Any]]] = {}

    def add(self, session_id: str, role: str, content: str, **metadata: Any) -> None:
        if session_id not in self._store:
            self._store[session_id] = []
        self._store[session_id].append({"role": role, "content": content, **metadata})

    def get(self, session_id: str, last_n: int | None = None) -> list[dict[str, Any]]:
        messages = self._store.get(session_id, [])
        return messages[-last_n:] if last_n else messages

    def clear(self, session_id: str) -> None:
        self._store.pop(session_id, None)
