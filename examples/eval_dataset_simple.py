"""Simple dataset evaluation example with Gentrace."""

import os
import asyncio
from typing import List, Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel

from gentrace import TestCase, init, experiment, eval_dataset, test_cases_async

load_dotenv()

init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)

PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "")
DATASET_ID = os.getenv("GENTRACE_DATASET_ID", "")

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class QueryInputs(BaseModel):
    query: str


async def process_ai_request(test_case: TestCase) -> Optional[str]:
    """Process AI request using OpenAI."""
    query = test_case.inputs.get("query", "Hey, how are you?")

    # Call OpenAI
    response = await openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": str(query)}],
    )

    return response.choices[0].message.content


@experiment()
async def dataset_evaluation() -> None:
    """Run evaluation on a dataset."""

    async def fetch_test_cases() -> List[TestCase]:
        """Fetch test cases from the dataset."""
        test_case_list = await test_cases_async.list(dataset_id=DATASET_ID)
        return test_case_list.data

    await eval_dataset(
        data=fetch_test_cases,
        schema=QueryInputs,
        interaction=process_ai_request,
    )

    print("Dataset evaluation completed! Check your Gentrace dashboard for results.")


if __name__ == "__main__":
    result = asyncio.run(dataset_evaluation())

    if result:
        print(f"Experiment URL: {result.url}")
