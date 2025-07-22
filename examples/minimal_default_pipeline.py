"""Minimal example demonstrating the use of @interaction decorator without explicit pipeline ID."""
# mypy: ignore-errors

import os
import asyncio

from openai import OpenAI

from gentrace import init, interaction

init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api")
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Simple AI function that will emit to the default pipeline
@interaction()
async def ask_ai(question: str) -> str:
    """Process a question with simulated AI processing."""
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": question}])
    return response.choices[0].message.content or ""


async def main():
    print("\n🚀 Running minimal example with default pipeline...\n")
    
    response = await ask_ai("What is the meaning of life?")
    print("Response:", response)
    
    # Give time for spans to be exported
    print("\n⏳ Waiting for spans to be exported...")
    await asyncio.sleep(2)
    
    print("\n✅ Done! Check your Postgres GTSpan table.")
    print('Expected: 1 span with pipelineId = "default"')
        

if __name__ == "__main__":
    asyncio.run(main())
