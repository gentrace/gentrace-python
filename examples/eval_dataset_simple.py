"""Simple dataset evaluation example with Gentrace."""

import os
import asyncio
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import AsyncOpenAI

from gentrace import TestCase, init, experiment, interaction, eval_dataset, test_cases_async

load_dotenv()

init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "")
DATASET_ID = os.getenv("GENTRACE_DATASET_ID", "")

openai = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def process_ai_request(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Process AI request using OpenAI."""
    # test_case.name # throwing exception

    # Extract the prompt from inputs
    prompt = inputs.get("prompt", "Hello, how are you?")
    
    # Call OpenAI
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    
    result = response.choices[0].message.content
    
    return {
        "result": result,
        "metadata": {
            "model": response.model,
            "usage": response.usage.model_dump() if response.usage else None
        }
    }


@interaction(pipeline_id=PIPELINE_ID, name="Process AI Request")
async def traced_process_ai_request(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Traced version of process_ai_request."""
    return await process_ai_request(inputs)


@experiment(pipeline_id=PIPELINE_ID)
async def dataset_evaluation() -> None:

    """Run evaluation on a dataset."""
    async def fetch_test_cases() -> List[TestCase]:
        """Fetch test cases from the dataset."""
        test_case_list = await test_cases_async.list(dataset_id=DATASET_ID)
        return test_case_list.data

    await eval_dataset(
        data=fetch_test_cases,
        interaction=traced_process_ai_request,
    )

    print("Dataset evaluation completed! Check your Gentrace dashboard for results.")


if __name__ == "__main__":
    # Run the experiment
    asyncio.run(dataset_evaluation())
