from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class TaskDefinition(BaseModel):
    task_id: str
    name: str
    description: str
    agent_name: str
    input_data: dict[str, Any] = {}
    priority: int = 0
    timeout_seconds: int = 300
    retry_policy: dict[str, Any] = {"max_retries": 2, "backoff_factor": 2.0}
