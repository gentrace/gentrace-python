"""
Simple Pydantic AI example with Gentrace tracing.

Pydantic AI uses OpenTelemetry internally, so Gentrace automatically
captures its traces when initialized.
"""

import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from gentrace import init, interaction

Agent.instrument_all()

load_dotenv()

# Initialize Gentrace (will capture Pydantic AI's OTEL traces)
init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

# Create a simple Pydantic AI agent
agent = Agent(
    OpenAIModel("gpt-4.1-nano"),
    system_prompt="You are a helpful assistant that gives concise answers.",
)


@interaction(name="pydantic_ai_chat", pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", ""))
async def chat_with_agent(prompt: str) -> str:
    result = await agent.run(prompt) # type: ignore
    return result.output


if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        response = await chat_with_agent("What is 2+2?")
        print(f"Agent says: {response}")

    asyncio.run(main())
