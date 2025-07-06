"""
Simple Anthropic Claude example with Gentrace tracing.
"""

import os

import anthropic
from dotenv import load_dotenv

from gentrace import init, interaction

load_dotenv()

# Initialize Gentrace
init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

# Initialize Anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@interaction(name="claude_chat", pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", ""))
def chat_with_claude(prompt: str) -> str:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022", messages=[{"role": "user", "content": prompt}], max_tokens=100
    )
    # Anthropic responses have TextBlock type
    from anthropic.types import TextBlock

    content = response.content[0]
    if isinstance(content, TextBlock):
        return content.text
    return str(content)


if __name__ == "__main__":
    result = chat_with_claude("Say hello in 3 words")
    print(f"Claude says: {result}")
