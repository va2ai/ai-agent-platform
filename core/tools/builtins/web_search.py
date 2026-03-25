from __future__ import annotations

from pydantic import BaseModel

from ..base import BaseTool, ToolOutput


class WebSearchInput(BaseModel):
    query: str
    max_results: int = 5


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for information"
    safety_level = "safe"

    def input_schema(self) -> type[BaseModel]:
        return WebSearchInput

    async def execute(self, input_data: BaseModel) -> ToolOutput:
        # Placeholder — integrate with your preferred search API
        return ToolOutput(success=True, result=f"Search results for: {input_data.query}")
