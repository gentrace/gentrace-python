"""
This example script demonstrates how to use the Gentrace Python SDK
to interact with test cases. It covers listing test cases from a dataset.

To run this example, ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g., https://gentrace.ai/api).
    GENTRACE_DATASET_ID: The ID of the dataset to list test cases from.
"""

import os
import asyncio

from gentrace import init, test_cases_async

api_key = os.getenv("GENTRACE_API_KEY")
base_url = os.getenv("GENTRACE_BASE_URL")
dataset_id = os.getenv("GENTRACE_DATASET_ID")


async def main() -> None:
    if not api_key:
        raise ValueError("GENTRACE_API_KEY environment variable not set.")

    if not base_url:
        raise ValueError("GENTRACE_BASE_URL environment variable not set.")

    if not dataset_id:
        raise ValueError("GENTRACE_DATASET_ID environment variable not set.")

    init(
        api_key=api_key,
        base_url=base_url,
    )

    response = await test_cases_async.list(dataset_id=dataset_id)
    for test_case in response.data:
        print(test_case.inputs)


if __name__ == "__main__":
    asyncio.run(main())
