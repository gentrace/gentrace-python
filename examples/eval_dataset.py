"""
This example script demonstrates how to use the Gentrace Python SDK's
eval_dataset() feature to evaluate a function against a set of test cases.
It showcases:

- Setting up Gentrace and OpenTelemetry for tracing.
- Defining test inputs and an interaction function.
- Using eval_dataset() with test cases provided as a lambda, an async function,
  and a sync function.

To run this example, ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g. https://gentrace.ai/api).
"""

import os
import atexit
import asyncio
from typing import Dict, Sequence
from typing_extensions import TypedDict

from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from gentrace import TestCase, TestInput, init, experiment, test_cases, eval_dataset, test_cases_async

gentrace_api_key = os.getenv("GENTRACE_API_KEY", "")
gentrace_base_url = os.getenv("GENTRACE_BASE_URL", "")
dataset_id = os.getenv("GENTRACE_DATASET_ID", "")
pipeline_id = os.getenv("GENTRACE_PIPELINE_ID", "")

if not gentrace_api_key:
    raise ValueError("GENTRACE_API_KEY environment variable not set.")

if not gentrace_base_url:
    raise ValueError(
        "GENTRACE_BASE_URL environment variable not set. Please set it to your Gentrace API endpoint (e.g., https://gentrace.ai/api)."
    )

if not dataset_id:
    raise ValueError("GENTRACE_DATASET_ID environment variable not set.")

if not pipeline_id:
    raise ValueError("GENTRACE_PIPELINE_ID environment variable not set.")

init(api_key=gentrace_api_key, base_url=gentrace_base_url)


class QueryInputsSchema(BaseModel):
    query: str


class QueryInputs(TypedDict):
    query: str


def interaction(inputs: QueryInputs) -> str:
    return f"Processed message '{inputs['query']}'"


async def fetch_test_cases() -> Sequence[TestCase]:
    """Fetches test cases from the specified dataset."""
    response = await test_cases_async.list(dataset_id=dataset_id)
    return response.data


@experiment(pipeline_id=pipeline_id)
async def run_my_simple_evaluation() -> None:
    print("Starting simple dataset evaluation...")

    print("Step 1: Using lambda to fetch test cases")
    await eval_dataset(
        data=lambda: [
            TestInput[QueryInputs](name="Test Case 1: Welcome Message", inputs={"query": "Hello, World!"}),
            TestInput[QueryInputs](name="Test Case 2: User Query", inputs={"query": "How does this work?"}),
            TestInput[QueryInputs](name="Test Case 3: Empty Message (for testing)", inputs={"query": ""}),
            TestInput[QueryInputs](name="Test Case 4: Extra Info", inputs={"query": "Test with extra"}),
        ],
        interaction=interaction,
        schema=QueryInputsSchema,
    )

    print("Step 2: Using async function to fetch test cases")
    await eval_dataset(data=fetch_test_cases, interaction=interaction, schema=QueryInputsSchema)

    print("Step 3: Using sync function to fetch test cases")
    await eval_dataset(
        data=lambda: test_cases.list(dataset_id=dataset_id).data, interaction=interaction, schema=QueryInputsSchema
    )

    print("\nEvaluation complete. Check your Gentrace dashboard for detailed traces.")


async def main_async_runner() -> None:
    """Runs the main evaluation logic."""
    await run_my_simple_evaluation()


if __name__ == "__main__":
    print("--- Example: eval_dataset Simple Usage ---")

    # OpenTelemetry Setup
    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)

    otlp_headers: Dict[str, str] = {}

    if gentrace_api_key:
        otlp_headers["Authorization"] = f"Bearer {gentrace_api_key}"

    span_exporter = OTLPSpanExporter(endpoint=f"{gentrace_base_url}/otel/v1/traces", headers=otlp_headers)

    span_processor = SimpleSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(span_processor)

    # Ensure OTel SDK is shutdown gracefully to flush traces
    atexit.register(tracer_provider.shutdown)
    print("OpenTelemetry OTLPSpanExporter initialized and SDK shutdown handler registered.")

    print("Running example...")

    try:
        asyncio.run(main_async_runner())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            # This can happen if running in an environment like Jupyter
            # where an event loop is already running.
            loop = asyncio.get_running_loop()
            loop.create_task(main_async_runner())
        else:
            raise

    print("--- Example Run Finished ---")
