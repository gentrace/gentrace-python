"""
Simple OpenAI example with Gentrace tracing.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from gentrace import init, interaction

load_dotenv()

# Initialize Gentrace
init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@interaction(name="chat_completion", pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", ""))
def chat_with_openai(prompt: str) -> str:
    response = client.chat.completions.create(model="gpt-4.1-nano", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    result = chat_with_openai("Say hello in 3 words")
    print(f"OpenAI says: {result}")
