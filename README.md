# ai-agent-platform

Multi-agent AI application built with a model-agnostic, framework-portable architecture.
Powered by Google Gemini 2.5 Pro / 2.5 Flash.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # add your Google API key
python examples/simple_chat/main.py  # test with mock provider
uvicorn apps.api.main:app --reload  # start the API
```

## Architecture

- **LLM providers** are pluggable via `LLMClient` protocol (Gemini 2.5 Pro/Flash configured)
- **Agent runtimes** are pluggable via `AgentRuntime` protocol (custom runtime included)
- **Vector stores** are pluggable via `VectorStore` protocol (pgvector configured)
- **Tools** go through a central gateway with validation and logging
- **Observability** tracks tokens, cost, latency, and tool calls (OpenTelemetry)
- **Memory** provides session, working, and long-term memory layers

## Philosophy

Own the contracts, abstract the runtimes, isolate the vendors, treat agent libraries as plugins.
