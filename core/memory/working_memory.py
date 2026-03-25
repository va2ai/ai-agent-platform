from __future__ import annotations

from typing import Any


class WorkingMemory:
    """Temporary scratch space for intermediate results within a workflow run."""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    def set(self, run_id: str, key: str, value: Any) -> None:
        if run_id not in self._store:
            self._store[run_id] = {}
        self._store[run_id][key] = value

    def get(self, run_id: str, key: str, default: Any = None) -> Any:
        return self._store.get(run_id, {}).get(key, default)

    def get_all(self, run_id: str) -> dict[str, Any]:
        return self._store.get(run_id, {})

    def clear(self, run_id: str) -> None:
        self._store.pop(run_id, None)
