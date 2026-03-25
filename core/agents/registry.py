from __future__ import annotations


class AgentDefinition:
    def __init__(self, name: str, description: str, system_prompt: str, tools: list[str] | None = None, model: str | None = None) -> None:
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.tools = tools or []
        self.model = model


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, AgentDefinition] = {}

    def register(self, agent: AgentDefinition) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> AgentDefinition:
        if name not in self._agents:
            raise KeyError(f"Agent '{name}' not registered. Available: {list(self._agents)}")
        return self._agents[name]

    def list_agents(self) -> list[dict[str, str]]:
        return [{"name": a.name, "description": a.description} for a in self._agents.values()]


agent_registry = AgentRegistry()
