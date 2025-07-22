"""Simple dataset evaluation example with Gentrace using local test cases.

This example demonstrates the clean new API where:
- TestInput is a Pydantic model for creating local test cases
- The interaction function always receives a TestCase object
- No Union types or isinstance checks needed
"""

import os
import asyncio
from typing import Any, Dict

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


@interaction(pipeline_id=PIPELINE_ID, name="Process AI Request")
async def process_ai_request(test_case: TestCase) -> Dict[str, Any]:
    """Process AI request using OpenAI.
    
    Clean API - the interaction function always receives a TestCase object,
    regardless of whether you pass TestInput, dict, or TestCase to eval_dataset.
    """
    # Direct access to test case properties - no isinstance checks!
    prompt = test_case.inputs.get("prompt", "Hey, how are you?")
    
    print(f"Running test case: {test_case.name}")

    # Call OpenAI
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": str(prompt)}], 
    )

    result = response.choices[0].message.content

    return {
        "result": result,
        "test_name": test_case.name,  # Can access test metadata
        "metadata": {"model": response.model, "usage": response.usage.model_dump() if response.usage else None},
    }


@experiment(pipeline_id=PIPELINE_ID)
async def dataset_evaluation() -> None:
    """Run evaluation on a dataset using local TestInput objects."""

    # Create test cases using the clean TestInput Pydantic model
    test_cases = [
        TestInput(
            name="greeting", 
            inputs={"prompt": "Hello! How are you doing today?"}
        ),
        TestInput(
            name="factual_question", 
            inputs={"prompt": "What is the capital of France?"}
        ),
        TestInput(
            name="math_problem", 
            inputs={"prompt": "What is 25 * 4?"}
        ),
        TestInput(
            name="creative_writing", 
            inputs={"prompt": "Write a haiku about artificial intelligence"}
        ),
        # Minimal example - only inputs is required
        TestInput(inputs={"prompt": "Tell me a joke"})
    ]
    
    await eval_dataset(
        data=test_cases,
        interaction=process_ai_request,  # Clean function signature - always receives TestCase
        max_concurrency=30,
    )

    print("Dataset evaluation completed! Check your Gentrace dashboard for results.")


if __name__ == "__main__":
    result = asyncio.run(dataset_evaluation())
    
    if result:
        print(f"Experiment URL: {result.url}")
