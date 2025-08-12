"""Simple dataset evaluation example with Gentrace using local test cases."""

import os
import asyncio
from typing import Optional
from typing_extensions import TypedDict

from dotenv import load_dotenv
from openai import AsyncOpenAI

from gentrace import TestCase, TestInput, init, experiment, eval_dataset

load_dotenv()

init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "")
DATASET_ID = os.getenv("GENTRACE_DATASET_ID", "")

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class PromptInputs(TypedDict):
    prompt: str


async def process_ai_request(test_case: TestCase) -> Optional[str]:
    prompt = test_case.inputs.get("prompt")

    response = await openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": str(prompt)}],
    )

    return response.choices[0].message.content


@experiment(pipeline_id=PIPELINE_ID)
async def dataset_evaluation() -> None:
    """Run evaluation on a dataset using type-safe TestInput objects with TypedDict."""

    # Using TestInput with TypedDict for type safety
    test_cases = [
        TestInput[PromptInputs](
            name="greeting", inputs={"prompt": "Hello! How are you doing today?"}
        ),
        TestInput[PromptInputs](
            name="factual_question", inputs={"prompt": "What is the capital of France?"}
        ),
        TestInput[PromptInputs](
            name="math_problem", inputs={"prompt": "What is 25 * 4?"}
        ),
        TestInput[PromptInputs](
            name="creative_writing",
            inputs={"prompt": "Write a haiku about artificial intelligence"},
        ),
        TestInput[PromptInputs](inputs={"prompt": "Tell me a joke"}),
    ]

    await eval_dataset(
        data=test_cases,
        schema=PromptInputs,
        interaction=process_ai_request,
    )

    print("Dataset evaluation completed! Check your Gentrace dashboard for results.")


if __name__ == "__main__":
    asyncio.run(dataset_evaluation())
