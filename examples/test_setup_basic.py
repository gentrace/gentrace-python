"""
Minimal example to test that spans are being sent to Gentrace.
"""

import os
import time

from opentelemetry import trace

import gentrace
from gentrace import setup, interaction


def main() -> None:
    # Initialize Gentrace
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
    )
    
    # Setup OpenTelemetry - that's it!
    setup()
    
    print("OpenTelemetry setup complete!")
    
    # Create a simple traced function
    @interaction(
        name="test_function", 
        pipeline_id=os.getenv("GENTRACE_PIPELINE_ID", "26d64c23-e38c-56fd-9b45-9adc87de797b")
    )
    def process_data(data: str) -> str:
        print(f"Processing: {data}")
        # Simulate some work
        time.sleep(0.1)
        return f"Processed: {data}"
    
    # Get a tracer
    tracer = trace.get_tracer(__name__)
    
    # Create a parent span
    with tracer.start_as_current_span("main_operation") as span:
        span.set_attribute("user.id", "test-user-123")
        span.set_attribute("operation.type", "test")
        
        # Call our traced function
        result = process_data("Hello, Gentrace!")
        
        span.set_attribute("result", result)
        span.add_event("Processing completed")
    
    print(f"Result: {result}")
    print("\nWaiting for spans to export...")
    
    # Give time for spans to export
    time.sleep(3)
    print("Done!")


if __name__ == "__main__":
    main()