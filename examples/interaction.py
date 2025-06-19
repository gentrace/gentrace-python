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
import asyncio

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion

import gentrace
from gentrace import GentraceSampler, traced, interaction

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

# Initialize Gentrace with automatic OpenTelemetry configuration
gentrace.init(
    api_key=api_key,
    base_url=gentrace_base_url,
    otel_setup={
        "service_name": "my-otel-interaction-example-app",
        "sampler": GentraceSampler()
    }
)

client = OpenAI(api_key=openai_api_key)
async_client = AsyncOpenAI(api_key=openai_api_key)


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
    asyncio.run(main())
