"""Simple dataset evaluation example with Gentrace."""

import os
import asyncio
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Make sure you import TestCase from gentrace.types for clarity
from gentrace import TestCase, TestInput, init, experiment, interaction, eval_dataset, test_cases_async

load_dotenv()

init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "26d64c23-e38c-56fd-9b45-9adc87de797b")
DATASET_ID = os.getenv("GENTRACE_DATASET_ID", "")

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))



@interaction(pipeline_id=PIPELINE_ID, name="Process AI Request")
async def process_ai_request(test_case: TestCase) -> Dict[str, Any]:
    """Process AI request using OpenAI."""
    # Clean API - no isinstance checks needed!
    prompt = test_case.inputs.get("prompt", "Hey, how are you?")

    # Call OpenAI
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": str(prompt)}],
    )

    result = response.choices[0].message.content

    return {
        "result": result,
        "metadata": {"model": response.model, "usage": response.usage.model_dump() if response.usage else None},
    }

# 2. The separate traced_process_ai_request function is no longer needed and has been removed.

@experiment(pipeline_id=PIPELINE_ID)
async def dataset_evaluation() -> None:
    """Run evaluation on a dataset."""

    async def fetch_test_cases() -> List[TestCase]:
        """Fetch test cases from the dataset."""
        test_case_list = await test_cases_async.list(dataset_id=DATASET_ID)
        return test_case_list.data

    await eval_dataset(
        data=fetch_test_cases,
        interaction=process_ai_request,
        max_concurrency=30,
    )

    print("Dataset evaluation completed! Check your Gentrace dashboard for results.")


@experiment(pipeline_id=PIPELINE_ID)
async def local_dataset_evaluation() -> None:
    """Run evaluation with local test cases using TestInput."""
    
    # Create local test cases using TestInput
    local_test_cases = [
        TestInput(
            name="Simple greeting",
            inputs={"prompt": "Hello, how are you?"}
        ),
        TestInput(
            name="Technical question",
            inputs={"prompt": "Explain quantum computing in simple terms"}
        ),
        TestInput(
            name="Math problem",
            inputs={"prompt": "What is 2 + 2?"}
        ),
        # Name is optional - will default to "Unnamed Test"
        TestInput(
            inputs={"prompt": "What's the weather like?"}
        )
    ]
    
    # Same clean API - process_ai_request receives TestCase objects
    await eval_dataset(
        data=local_test_cases,
        interaction=process_ai_request,
        max_concurrency=3,
    )
    
    print("Local dataset evaluation completed!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "local":
        # Run with local test cases
        print("Running with local test cases...")
        asyncio.run(local_dataset_evaluation())
    else:
        # Run with dataset from Gentrace
        print("Running with dataset from Gentrace...")
        asyncio.run(dataset_evaluation())