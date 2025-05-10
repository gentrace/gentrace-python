import asyncio
import atexit
import os
from typing import Dict

from gentrace.lib.interaction import interaction # Changed import to get the function directly

# OpenTelemetry API and SDK components
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,  # Or BatchSpanProcessor
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# 1. Initialize a Resource (optional, but good practice)
resource = Resource(attributes={
    "service.name": "my-otel-interaction-example-app"
})

# 2. Initialize a TracerProvider
tracer_provider = TracerProvider(resource=resource)

# 3. Configure a Span Exporter
# Define the API key (ideally from an environment variable)
api_key = os.getenv("GENTRACE_API_KEY")
otlp_headers: Dict[str, str] = {} # Type hint and ensure it's always a dict
if api_key:
    otlp_headers["Authorization"] = f"Bearer {api_key}"

span_exporter = OTLPSpanExporter(
    endpoint="http://localhost:3000/api/otel/v1/traces", # Ensure this endpoint is correct for Gentrace
    headers=otlp_headers
)

# 4. Configure a Span Processor
span_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)

# 5. Set the global TracerProvider
trace.set_tracer_provider(tracer_provider)

PIPELINE_ID = '26d64c23-e38c-56fd-9b45-9adc87de797b'

@interaction(pipeline_id=PIPELINE_ID, name="my_sync_interaction_example", attributes={"custom_attr": "sync_value"})
def my_synchronous_interaction(x: int, y: int) -> int:
    print(f"Synchronous interaction called with {x} and {y}")
    result = x * y  # Different operation for distinction
    print(f"Synchronous interaction result: {result}")
    if result < 0:
        raise ValueError("Synchronous interaction result cannot be negative in this example")
    return result

@interaction(pipeline_id=PIPELINE_ID, name="my_async_interaction_example", attributes={"custom_attr": "async_value"})
async def my_asynchronous_interaction(name: str, delay: float = 0.1) -> str:
    print(f"Asynchronous interaction called with {name}")
    await asyncio.sleep(delay) # Simulate some async work
    result = f"Interacted with {name}!"
    if name == "error":
        raise RuntimeError("Asynchronous interaction encountered a simulated error")
    print(f"Asynchronous interaction result: {result}")
    return result

async def main() -> None:
    print("--- Running Synchronous Interaction ---")
    try:
        sync_result = my_synchronous_interaction(7, 3)
        print(f"Returned from synchronous interaction: {sync_result}\n") # Corrected EOL by adding closing quote
    except ValueError as e:
        print(f"Caught expected error from synchronous interaction: {e}\n") # Corrected EOL

    print("--- Running Asynchronous Interaction (Success) ---")
    async_result_success = await my_asynchronous_interaction("GentraceUser")
    print(f"Returned from asynchronous interaction (Success): {async_result_success}\n") # Corrected EOL

    print("--- Running Asynchronous Interaction (Error) ---")
    try:
        await my_asynchronous_interaction("error")
    except RuntimeError as e:
        print(f"Caught expected error from asynchronous interaction: {e}\n") # Corrected EOL


if __name__ == "__main__":
    # Ensure the tracer provider is shutdown on exit to flush spans
    atexit.register(tracer_provider.shutdown)
    print("Registered atexit handler for OpenTelemetry TracerProvider shutdown.")

    print("\nRunning @interaction decorator examples...")
    
    asyncio.run(main())

    print("\nFinished running interaction examples.")
    print("Check your Gentrace dashboard (if configured and API key is set) to see the traces.") 