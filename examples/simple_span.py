import asyncio
import atexit
import os
from typing import Dict

# OpenTelemetry API and SDK components
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor, # Using BatchSpanProcessor
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# 1. Initialize a Resource (optional, but good practice)
resource = Resource(attributes={
    "service.name": "my-manual-otel-example-app"
})

# 2. Initialize a TracerProvider
tracer_provider = TracerProvider(resource=resource)

# 3. Configure a Span Exporter
api_key = os.getenv("GENTRACE_API_KEY")
otlp_headers: Dict[str, str] = {} # Use Dict for type hint
if api_key:
    otlp_headers["Authorization"] = f"Bearer {api_key}"

span_exporter = OTLPSpanExporter(
    endpoint="http://localhost:3000/api/otel/v1/traces", # Ensure this is your target endpoint
    headers=otlp_headers
)

# 4. Configure a Span Processor
# Using BatchSpanProcessor for better performance in most cases
span_processor = BatchSpanProcessor(span_exporter)
tracer_provider.add_span_processor(span_processor)

# 5. Set the global TracerProvider
trace.set_tracer_provider(tracer_provider)

# Get a tracer instance
tracer = trace.get_tracer(__name__)

def my_synchronous_function(x: int, y: int) -> int:
    # Manually create a span
    with tracer.start_as_current_span("my_manual_sync_span") as current_span:
        print(f"Synchronous function called with {x} and {y}")
        
        # Set simple attributes
        current_span.set_attribute("function.type", "synchronous")
        current_span.set_attribute("input.x", x)
        current_span.set_attribute("input.y", y)
        
        result = x + y
        
        current_span.set_attribute("output.result", result)
        print(f"Synchronous function result: {result}")
        
        # The span is automatically ended when exiting the 'with' block
    return result

async def my_asynchronous_function(name: str) -> str:
    # Manually create a span
    with tracer.start_as_current_span("my_manual_async_span") as current_span:
        print(f"Asynchronous function called with {name}")
        
        # Set simple attributes
        current_span.set_attribute("function.type", "asynchronous")
        current_span.set_attribute("input.name", name)
        
        await asyncio.sleep(0.1) # Simulate some async work
        result = f"Hello, {name}!"
        
        current_span.set_attribute("output.result", result)
        print(f"Asynchronous function result: {result}")
        
        # The span is automatically ended when exiting the 'with' block
    return result

async def main() -> None:
    # Example of calling the synchronous traced function
    with tracer.start_as_current_span("main_sync_call_span") as span:
        span.set_attribute("call.type", "synchronous_wrapper")
        sync_result = my_synchronous_function(5, 10)
        print(f"Returned from synchronous: {sync_result}\\n")

    # Example of calling the asynchronous traced function
    with tracer.start_as_current_span("main_async_call_span") as span:
        span.set_attribute("call.type", "asynchronous_wrapper")
        async_result = await my_asynchronous_function("World")
        print(f"Returned from asynchronous: {async_result}\\n")

    # Example of a very simple standalone span
    with tracer.start_as_current_span("standalone_simple_span") as span:
        span.set_attribute("example.category", "standalone")
        span.set_attribute("is.simple", True)
        print("Created and ended a standalone simple span.")
        await asyncio.sleep(0.05) # Simulate some work within this span
        span.set_attribute("status", "completed")


if __name__ == "__main__":
    # Ensure OTel SDK is shutdown gracefully to flush traces
    atexit.register(tracer_provider.shutdown)
    print("Registered OTel SDK shutdown handler with atexit.")

    print("Running manual OpenTelemetry span examples...")
    
    asyncio.run(main())

    print("\\nFinished running examples.")
    print("Check your OTLP endpoint (e.g., Jaeger, Gentrace dashboard) to see the traces.") 