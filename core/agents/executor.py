from __future__ import annotations

import logging
from typing import Any

from .contracts.agent_input import AgentInput
from .contracts.agent_output import AgentOutput
from .registry import agent_registry

logger = logging.getLogger(__name__)


class AgentExecutor:
    """Executes an agent task using the configured runtime."""

    def __init__(self, runtime) -> None:
        self._runtime = runtime

    async def run(self, agent_name: str, input_data: AgentInput) -> AgentOutput:
        agent_def = agent_registry.get(agent_name)
        logger.info("agent.start", extra={"agent": agent_name, "task": input_data.task})

        result = await self._runtime.run_task(
            agent_name=agent_name,
            payload=input_data.model_dump(),
            context={"system_prompt": agent_def.system_prompt, "tools": agent_def.tools, "model": agent_def.model},
        )

        output = AgentOutput(
            result=result.output.get("result", ""),
            status=result.status,
            steps=[],
            metadata={"run_id": result.run_id, "token_usage": result.token_usage, "latency_ms": result.latency_ms},
        )
        logger.info("agent.complete", extra={"agent": agent_name, "status": output.status})
        return output
