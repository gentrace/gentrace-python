"""Simple dataset evaluation example with Gentrace.

Key Changes:
- The interaction function in eval_dataset now receives the full test case object
  (TestCase with properties like id, name, inputs, expectedOutputs) instead of just the inputs
- This allows you to access test case metadata within your evaluation logic
"""

import os
import asyncio
from typing import Any, Dict, List, Union

from dotenv import load_dotenv
from openai import AsyncOpenAI

from gentrace import TestCase, TestInput, init, experiment, interaction, eval_dataset, test_cases_async

load_dotenv()

init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "")
DATASET_ID = os.getenv("GENTRACE_DATASET_ID", "")

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def process_ai_request(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Process AI request using OpenAI."""
    # Extract the prompt from inputs
    prompt = inputs.get("prompt", "Hey, how are you?")

    # Call OpenAI
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.choices[0].message.content

    return {
        "result": result,
        "metadata": {"model": response.model, "usage": response.usage.model_dump() if response.usage else None},
    }


@experiment(pipeline_id=PIPELINE_ID)
async def dataset_evaluation() -> None:
    """Run evaluation on a dataset."""

    async def fetch_test_cases() -> List[TestCase]:
        """Fetch test cases from the dataset."""
        test_case_list = await test_cases_async.list(dataset_id=DATASET_ID)
        return test_case_list.data

    # The interaction function now receives the full test case object
    async def process_test_case(test_case: Union[TestCase, TestInput[Dict[str, Any]]]) -> Dict[str, Any]:
        """Process a single test case with full access to test case metadata."""
        # Access test case properties like id, name, inputs, expectedOutputs, etc.
        if isinstance(test_case, TestCase):
            print(f"Running test case: {test_case.name} (ID: {test_case.id})")
            name = test_case.name
            inputs = test_case.inputs
        else:
            # TestInput case
            name = test_case.get('name', 'unnamed')
            print(f"Running test case: {name}")
            inputs = test_case.get('inputs', {})
        
        # Use the traced version of process_ai_request
        traced_fn = interaction(
            pipeline_id=PIPELINE_ID,
            name=f"Process AI Request - {name}"
        )(process_ai_request)
        
        # Pass only the inputs to the actual function
        return await traced_fn(inputs)

    await eval_dataset(
        data=fetch_test_cases,
        interaction=process_test_case,
        max_concurrency=30,
    )

    print("Dataset evaluation completed! Check your Gentrace dashboard for results.")


if __name__ == "__main__":
    # Run the experiment
    result = asyncio.run(dataset_evaluation())
    print(f"Experiment URL: {result.url}")
