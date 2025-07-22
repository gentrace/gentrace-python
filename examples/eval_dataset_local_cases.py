"""Simple dataset evaluation example with Gentrace using local test cases.

This example demonstrates the clean new API where:
- TestInput is a generic Pydantic model that can accept TypedDict for type safety
- The interaction function always receives a TestCase object
- Type-safe inputs using TypedDict
"""

import os
import asyncio
from typing import Optional
from typing_extensions import TypedDict

from dotenv import load_dotenv
from openai import AsyncOpenAI

from gentrace import TestCase, TestInput, init, experiment, interaction, eval_dataset

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



@interaction(pipeline_id=PIPELINE_ID, name="Process AI Request")
async def process_ai_request(test_case: TestCase) -> Optional[str]:
    print(f"Running test case: {test_case.name}")

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
            name="greeting", 
            inputs={"prompt": "Hello! How are you doing today?"}
        ),
        TestInput[PromptInputs](
            name="factual_question", 
            inputs={"prompt": "What is the capital of France?"}
        ),
        TestInput[PromptInputs](
            name="math_problem", 
            inputs={"prompt": "What is 25 * 4?"}
        ),
        TestInput[PromptInputs](
            name="creative_writing", 
            inputs={"prompt": "Write a haiku about artificial intelligence"}
        ),
        TestInput[PromptInputs](
            inputs={"prompt": "Tell me a joke"}
        )
    ]
    
    # Note: You can also use TestInput without TypedDict for backward compatibility:
    # TestInput(name="example", inputs={"prompt": "Hello", "any_field": "value"})
    
    await eval_dataset(
        data=test_cases,
        interaction=process_ai_request,
    )

    print("Dataset evaluation completed! Check your Gentrace dashboard for results.")


if __name__ == "__main__":
    result = asyncio.run(dataset_evaluation())
    
    if result:
        print(f"Experiment URL: {result.url}")
