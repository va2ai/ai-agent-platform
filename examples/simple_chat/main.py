"""Simple single-agent chat loop using a mock LLM provider.

Run: python examples/simple_chat/main.py

No API keys required.
"""
from __future__ import annotations

import asyncio

from .mock_provider import MockLLMClient


async def chat_loop():
    client = MockLLMClient()

    print("=" * 60)
    print("  Simple Chat — Mock LLM Provider")
    print("  Type 'quit' to exit")
    print("=" * 60)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        response = await client.generate(
            user_input,
            system="You are a helpful assistant.",
        )

        print(f"AI:  {response.content}")
        print(f"     [{response.input_tokens} in / {response.output_tokens} out tokens, {response.latency_ms:.1f}ms]")
        print()


def main():
    asyncio.run(chat_loop())


if __name__ == "__main__":
    main()
