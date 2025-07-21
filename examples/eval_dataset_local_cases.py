"""Simple dataset evaluation example with Gentrace using local test cases.

Key Changes:
- The interaction function in eval_dataset now receives the full test case object
  (TestInput with properties like name, inputs) instead of just the inputs
- This allows you to access test case metadata within your evaluation logic
"""

import os
import asyncio
from typing import Any, Dict, Union

from dotenv import load_dotenv
from openai import AsyncOpenAI

from gentrace import TestInput, init, experiment, interaction, eval_dataset
from gentrace.types import TestCase

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

    # The interaction function now receives the full test case object
    async def process_test_case(test_case: Union[TestCase, TestInput[Dict[str, Any]]]) -> Dict[str, Any]:
        """Process a single test case with full access to test case metadata."""
        # Access test case properties like name and inputs
        name = test_case.get('name', 'unnamed') if isinstance(test_case, dict) else test_case.name
        inputs = test_case.get('inputs', {}) if isinstance(test_case, dict) else test_case.inputs
        
        print(f"Running test case: {name}")
        
        # Use the traced version of process_ai_request
        traced_fn = interaction(
            pipeline_id=PIPELINE_ID,
            name=f"Process AI Request - {name}"
        )(process_ai_request)
        
        # Pass only the inputs to the actual function
        return await traced_fn(inputs)

    await eval_dataset(
        data=[
            TestInput(name="greeting", inputs={"prompt": "Hello! How are you doing today?"}),
            TestInput(name="factual_question", inputs={"prompt": "What is the capital of France?"}),
            TestInput(name="math_problem", inputs={"prompt": "What is 25 * 4?"}),
            TestInput(name="creative_writing", inputs={"prompt": "Write a haiku about artificial intelligence"}),
        ],
        interaction=process_test_case,
        max_concurrency=30,
    )

    print("Dataset evaluation completed! Check your Gentrace dashboard for results.")


if __name__ == "__main__":
    # Run the experiment
    result = asyncio.run(dataset_evaluation())
    print(f"Experiment URL: {result.url}")
