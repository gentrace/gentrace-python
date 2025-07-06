"""
OpenAI instrumentation example using OpenInference with Gentrace.

This example uses the OpenInference instrumentation library instead of the official
OpenTelemetry contrib package (opentelemetry-instrumentation-openai-v2) because:

1. OpenInference captures full input/output content - The official OpenTelemetry
   package doesn't include message content or responses for privacy reasons.

2. Simplified integration - OpenInference is designed specifically for LLM
   observability and provides richer telemetry data out of the box.

Shows how OpenInference OpenAI instrumentation works with Gentrace's @interaction decorator.
"""

import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openinference.instrumentation.openai import OpenAIInstrumentor

from gentrace import init, interaction

load_dotenv()

# Pipeline ID for tracking
PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "26d64c23-e38c-56fd-9b45-9adc87de797b")

# Initialize Gentrace with OpenAI instrumentation
init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
    otel_setup={"service_name": "openai-instrumentation-demo", "instrumentations": [OpenAIInstrumentor()]},
)

# Create async client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@interaction(name="summarize_text", pipeline_id=PIPELINE_ID)
async def summarize(text: str) -> str:
    """Summarize text using OpenAI - automatically traced."""
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
            {"role": "user", "content": f"Summarize this text in one sentence: {text}"},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content or ""


async def main() -> None:
    text = "OpenTelemetry is a collection of tools, APIs, and SDKs used to instrument, generate, collect, and export telemetry data to help you analyze your software's performance and behavior."

    summary = await summarize(text)
    print(f"Summary: {summary}")
    print("\n✓ Both the @interaction and OpenAI calls have been traced!")

    # Give time for spans to export
    await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
