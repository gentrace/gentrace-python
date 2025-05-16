"""
This example script demonstrates a combined usage of various Gentrace Python SDK features,
including @eval, @interaction, and eval_dataset within a single @experiment.
It showcases:

- Setting up Gentrace and OpenTelemetry for tracing.
- Defining an experiment that orchestrates multiple evaluation types.
- Using `eval_dataset` for batch evaluations against a dataset.
- Using the `@eval` decorator for individual, ad-hoc evaluation steps (both sync and async).
- Using the `@interaction` decorator to trace specific function calls as part of the experiment.

To run this example, ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g., https://gentrace.ai/api).
    GENTRACE_DATASET_ID: (Optional) The ID of the dataset to use for `eval_dataset`.
    GENTRACE_PIPELINE_ID: The ID of the pipeline to associate with this experiment.
"""

import os
import atexit
import asyncio
from typing import Any, Dict
from typing_extensions import TypedDict

# OpenTelemetry API and SDK components
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from gentrace import TestInput, eval, init, experiment, interaction, eval_dataset

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

if not pipeline_id:
    raise ValueError("GENTRACE_PIPELINE_ID environment variable not set.")

resource = Resource(attributes={"service.name": "example-combined-eval"})

tracer_provider = TracerProvider(resource=resource)

otlp_headers: Dict[str, str] = {}
if gentrace_api_key:
    otlp_headers["Authorization"] = f"Bearer {gentrace_api_key}"
else:
    print("Warning: GENTRACE_API_KEY environment variable not set.")

span_exporter = OTLPSpanExporter(endpoint=f"{gentrace_base_url}/otel/v1/traces", headers=otlp_headers)

span_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)

trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)

init(api_key=gentrace_api_key, base_url=gentrace_base_url)


class InteractionInput(TypedDict):
    prompt: str
    temperature: float


class InteractionOutput(TypedDict):
    result: str


def dataset_interaction(inputs: InteractionInput) -> InteractionOutput:
    result_text = f"Interaction based on '{inputs['prompt'][:20]}...' at temp {inputs['temperature']}"
    return InteractionOutput(result=result_text)


@interaction(pipeline_id=pipeline_id, name="Simulated LLM Call")
async def simulated_llm_call(prompt: str, config: Dict[str, Any]) -> Dict[str, Any]:
    print(f"Running @interaction function with prompt: '{prompt[:30]}...'")
    await asyncio.sleep(0.15)
    response = {
        "completion": f"Generated text based on prompt: {prompt[:15]}...",
        "model_used": config.get("model", "default-model"),
        "tokens": len(prompt) // 4,
    }
    print("@interaction function finished.")
    return response


@experiment(pipeline_id=pipeline_id)
async def run_combined_evaluation() -> None:
    @eval(name="Individual Eval Step 1 (Sync)", metadata={"type": "simple_check", "value": 10})
    def individual_sync_eval(input_val: int) -> Dict[str, Any]:
        print(f"Running sync @eval function with input: {input_val}")
        return {"status": "completed", "input_received": input_val, "result_value": input_val * 2}

    await individual_sync_eval(10)

    @eval(name="Individual Eval Step 2 (Async)")
    async def individual_async_eval() -> str:
        print("Running async @eval function")
        await asyncio.sleep(0.1)
        return "Async evaluation finished successfully."

    await individual_async_eval()

    print(f"Starting combined evaluation for pipeline {pipeline_id}...")

    print("\nRunning eval_dataset...")
    dataset_results = await eval_dataset(
        data=lambda: [
            TestInput[InteractionInput](
                name="Sample Case 1", inputs={"prompt": "Write a story about a dragon.", "temperature": 0.7}
            ),
            TestInput[InteractionInput](
                name="Sample Case 2: Short Prompt", inputs={"prompt": "Summarize AI.", "temperature": 0.5}
            ),
        ],
        interaction=dataset_interaction,
    )
    print(f"eval_dataset completed. Results: {dataset_results}")

    interaction_result = await simulated_llm_call(
        prompt="Generate a creative summary of recent AI advancements.",
        config={"model": "fancy-ai-model-v3", "temperature": 0.6},
    )
    print(f"@interaction function returned: {interaction_result}")

    print("Combined evaluation steps initiated. Check Gentrace dashboard.")


async def main() -> None:
    await run_combined_evaluation()


if __name__ == "__main__":
    # Ensure OTel SDK is shutdown gracefully to flush traces
    atexit.register(tracer_provider.shutdown)
    print("Registered OTel SDK shutdown handler with atexit.")

    print("Running combined @eval and eval_dataset example...")

    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            loop = asyncio.get_running_loop()
            loop.create_task(main())
        else:
            raise

    print("Finished running combined example.")
    print("Check your Gentrace dashboard to see the traces.")
