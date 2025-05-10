import asyncio
import atexit
import os

from gentrace import traced #, init # init is commented out as it's not strictly needed for decorator demo

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
    "service.name": "my-otel-example-app"
})

# 2. Initialize a TracerProvider
# The SdkTracerProvider from opentelemetry.sdk.trace will automatically
# register its shutdown() method with atexit upon initialization.
# The explicit registration later is for demonstration of how one *would* do it.
tracer_provider = TracerProvider(resource=resource)

# 3. Configure a Span Exporter
# Define the API key (ideally from an environment variable)
# For example: api_key = os.getenv("GENTRACE_API_KEY", "YOUR_FALLBACK_API_KEY")
# Using a placeholder for this example if GENTRACE_API_KEY is not set.
api_key = os.getenv("GENTRACE_API_KEY")
otlp_headers = {
    "Authorization": f"Bearer {api_key}"
}
span_exporter = OTLPSpanExporter(
    endpoint="http://localhost:3000/api/otel/v1/traces",
    headers=otlp_headers
)

# 4. Configure a Span Processor
# SimpleSpanProcessor exports spans synchronously as they are ended.
# BatchSpanProcessor batches them and exports periodically/on flush/on shutdown.
# If using BatchSpanProcessor, shutdown is critical to flush the final batch.
span_processor = SimpleSpanProcessor(span_exporter)

tracer_provider.add_span_processor(span_processor)

# 5. Set the global TracerProvider
# This makes the configured tracer_provider available via opentelemetry.trace.get_tracer()
trace.set_tracer_provider(tracer_provider)

@traced(name="my_sync_function_example", attributes={"example_type": "synchronous"})
def my_synchronous_function(x: int, y: int) -> int:
    print(f"Synchronous function called with {x} and {y}")
    result = x + y
    print(f"Synchronous function result: {result}")
    return result

@traced(name="my_async_function_example", attributes={"example_type": "asynchronous"})
async def my_asynchronous_function(name: str) -> str:
    print(f"Asynchronous function called with {name}")
    await asyncio.sleep(0.1) # Simulate some async work
    result = f"Hello, {name}!"
    print(f"Asynchronous function result: {result}")
    return result

async def main() -> None:
    # Example of calling the synchronous traced function
    sync_result = my_synchronous_function(5, 10)
    print(f"Returned from synchronous: {sync_result}\n")

    # Example of calling the asynchronous traced function
    async_result = await my_asynchronous_function("World")
    print(f"Returned from asynchronous: {async_result}\n")

if __name__ == "__main__":
    atexit.register(tracer_provider.shutdown)
    print("Finished registering atexit handler.")

    # Note: For the traces to be sent to Gentrace, you'd need to have
    # the Gentrace SDK initialized (e.g., using `gentrace.init()`) and
    # OpenTelemetry configured to export spans.
    # This example primarily shows how to apply the decorator.
    print("Running @traced decorator examples...")
    
    asyncio.run(main())

    print("\nFinished running examples.")
    print("Check your Gentrace dashboard (if configured) to see the traces.") 