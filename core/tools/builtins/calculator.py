from __future__ import annotations

from pydantic import BaseModel

from ..base import BaseTool, ToolOutput


class CalculatorInput(BaseModel):
    expression: str


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate a mathematical expression"
    safety_level = "safe"

    def input_schema(self) -> type[BaseModel]:
        return CalculatorInput

    async def execute(self, input_data: BaseModel) -> ToolOutput:
        try:
            # Safe eval for basic math
            allowed = set("0123456789+-*/.() ")
            expr = input_data.expression
            if not all(c in allowed for c in expr):
                return ToolOutput(success=False, error="Invalid characters in expression")
            result = eval(expr)  # noqa: S307
            return ToolOutput(success=True, result=result)
        except Exception as e:
            return ToolOutput(success=False, error=str(e))
