"""
Comprehensive test to verify all aspects of span ingestion.
"""

import os
import time
from opentelemetry import trace

import gentrace
from gentrace import setup, interaction, traced

# Pipeline ID from environment
PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "26d64c23-e38c-56fd-9b45-9adc87de797b")


def main() -> None:
    # Initialize Gentrace
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
    )
    
    # Setup OpenTelemetry
    setup()
    
    print("Running comprehensive span test...")
    
    # Get a tracer
    tracer = trace.get_tracer(__name__)
    
    # Create a parent span
    with tracer.start_as_current_span("parent_operation") as parent:
        parent.set_attribute("test.type", "comprehensive")
        parent.add_event("Starting comprehensive test")
        
        # Create an interaction span (should be child of parent)
        @interaction(name="process_data", pipeline_id=PIPELINE_ID)
        def process(data: str) -> str:
            # Create a nested span inside the interaction
            with tracer.start_as_current_span("nested_operation") as nested:
                nested.set_attribute("data.length", len(data))
                time.sleep(0.05)  # Simulate work
                return f"Processed: {data}"
        
        # Create a traced function (should also be child of parent)
        @traced(name="helper_function")
        def helper(value: int) -> int:
            time.sleep(0.05)  # Simulate work
            return value * 2
        
        # Execute our functions
        result1 = process("Test data")
        result2 = helper(42)
        
        parent.add_event("Operations completed", {
            "result1": result1,
            "result2": result2
        })
    
    print(f"Results: {result1}, {result2}")
    print("\nWaiting for spans to export...")
    time.sleep(3)
    print("Done!")


if __name__ == "__main__":
    main()