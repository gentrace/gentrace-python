"""
Simple evaluation example using Gentrace @eval decorator.
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv

from gentrace import eval, init, experiment

load_dotenv()

# Initialize Gentrace
init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
)


# Define an evaluation function
@eval(name="length_check")
def check_response_length(output: str, expected_max_length: int = 50) -> float:
    """Evaluate if response is concise (under expected length)."""
    if len(output) <= expected_max_length:
        return 1.0
    else:
        return 0.0


# Run experiment with evaluation
@experiment(pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", ""), options={"name": "response_quality_test"})
async def test_response_quality() -> Dict[str, Any]:
    # Simulate some output
    output = "This is a test response"

    # Evaluate the output
    score = await check_response_length(output)
    print(f"Length check score: {score}")

    return {"output": output, "score": score}


if __name__ == "__main__":
    import asyncio

    result = asyncio.run(test_response_quality())
    print(f"Experiment URL: {result.url}")
