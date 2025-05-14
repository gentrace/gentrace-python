"""
This example script showcases the use of the Gentrace Python SDK to trace
and monitor interactions within an application. It demonstrates:
- Setting up OpenTelemetry for distributed tracing.
- Tracing synchronous and asynchronous calls to OpenAI's API.
- Utilizing Gentrace's @traced and @interaction decorators for enhanced observability.
- Handling both successful operations and simulated errors.

To run this example, ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    OPENAI_API_KEY:   Your OpenAI API key.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g., http://localhost:3000).
"""

import os
import atexit
import asyncio
from typing import Dict

from openai import OpenAI, AsyncOpenAI
from opentelemetry import trace
from openai.types.chat import ChatCompletion
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from gentrace import GentraceSampler, GentraceSpanProcessor, traced, interaction

resource = Resource(attributes={"service.name": "my-otel-interaction-example-app"})
tracer_provider = TracerProvider(resource=resource, sampler=GentraceSampler())

api_key = os.getenv("GENTRACE_API_KEY", "")
openai_api_key = os.getenv("OPENAI_API_KEY", "")
gentrace_base_url = os.getenv("GENTRACE_BASE_URL", "")
pipeline_id = os.getenv("GENTRACE_PIPELINE_ID", "")

if not api_key:
    raise ValueError("GENTRACE_API_KEY environment variable not set.")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
if not gentrace_base_url:
    raise ValueError("GENTRACE_BASE_URL environment variable not set.")

otlp_headers: Dict[str, str] = {}
if api_key:
    otlp_headers["Authorization"] = f"Bearer {api_key}"

span_exporter = OTLPSpanExporter(
    endpoint=f"{gentrace_base_url}/otel/v1/traces",
    headers=otlp_headers,
)

client = OpenAI(api_key=openai_api_key)
async_client = AsyncOpenAI(api_key=openai_api_key)

# Instantiate and add GentraceSpanProcessor to enrich spans with `gentrace.sample`
gentrace_baggage_processor = GentraceSpanProcessor()
tracer_provider.add_span_processor(gentrace_baggage_processor)

simple_export_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(simple_export_processor)
trace.set_tracer_provider(tracer_provider)


@traced(name="sync_openai_llm_call", attributes={"llm_vendor": "OpenAI", "llm_model": "gpt-4o"})
def sync_openai_llm_call(prompt: str) -> ChatCompletion:
    response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    return response


@traced(name="async_openai_llm_call", attributes={"llm_vendor": "OpenAI", "llm_model": "gpt-4o"})
async def async_openai_llm_call(prompt: str) -> ChatCompletion:
    response = await async_client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return response


@interaction(pipeline_id=pipeline_id, name="my_sync_interaction_example", attributes={"custom_attr": "sync_value"})
def my_synchronous_interaction(x: int, y: int) -> int:
    result = x * y
    llm_prompt = f"Summarize the result of a synchronous operation: {x} * {y} = {result}"
    llm_response = sync_openai_llm_call(llm_prompt)
    print("Final result:", llm_response)
    if result < 0:
        raise ValueError("Synchronous interaction result cannot be negative in this example")
    return result


@interaction(pipeline_id=pipeline_id, name="my_async_interaction_example", attributes={"custom_attr": "async_value"})
async def my_asynchronous_interaction(name: str, delay: float = 0.1) -> str:
    await asyncio.sleep(delay)
    llm_prompt = (
        f"Describe an asynchronous interaction with user '{name}' after a delay. Super concise, 10 words or less."
    )
    await async_openai_llm_call(llm_prompt)

    result = f"Interacted with {name}!"
    if name == "error":
        raise RuntimeError("Asynchronous interaction encountered a simulated error")
    return result


async def main() -> None:
    async_result_success = await my_asynchronous_interaction("GentraceUser")
    print("Final result:", async_result_success)
    try:
        await my_asynchronous_interaction("error")
    except RuntimeError as e:
        print(f"Caught expected error from asynchronous interaction: {e}\n")

    print("\nCheck the Gentrace dashboard to see all interactions and traces!")


if __name__ == "__main__":
    atexit.register(tracer_provider.shutdown)
    asyncio.run(main())
