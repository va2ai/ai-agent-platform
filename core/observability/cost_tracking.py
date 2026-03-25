from __future__ import annotations

from dataclasses import dataclass, field


# Approximate costs per 1M tokens (USD) — update as pricing changes
MODEL_COSTS: dict[str, tuple[float, float]] = {
    "gemini-3.1-pro-preview": (2.50, 15.00),
    "gemini-3-flash-preview": (0.15, 0.60),
    "gemini-3.1-flash-lite-preview": (0.05, 0.20),
    "gemini-2.5-pro": (1.25, 10.00),
    "gemini-2.5-flash": (0.15, 0.60),
}


@dataclass
class RunCost:
    run_id: str
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0


@dataclass
class CostTracker:
    runs: list[RunCost] = field(default_factory=list)

    def record(self, run_id: str, model: str, input_tokens: int, output_tokens: int) -> RunCost:
        input_rate, output_rate = MODEL_COSTS.get(model, (0.0, 0.0))
        cost = (input_tokens / 1_000_000 * input_rate) + (output_tokens / 1_000_000 * output_rate)
        run_cost = RunCost(run_id=run_id, model=model, input_tokens=input_tokens, output_tokens=output_tokens, estimated_cost_usd=round(cost, 6))
        self.runs.append(run_cost)
        return run_cost

    @property
    def total_cost(self) -> float:
        return sum(r.estimated_cost_usd for r in self.runs)

    @property
    def total_tokens(self) -> int:
        return sum(r.input_tokens + r.output_tokens for r in self.runs)


cost_tracker = CostTracker()
