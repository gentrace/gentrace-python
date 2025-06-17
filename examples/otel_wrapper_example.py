"""
Example demonstrating the usage of the setup wrapper function.

This example shows how to use the simplified OpenTelemetry setup wrapper
that eliminates boilerplate code.
"""

import os
from opentelemetry import trace

import gentrace
from gentrace import setup, interaction


def main():
    # Initialize Gentrace SDK
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL"),
    )
    
    # Example 1: Basic OTEL setup without Gentrace samplers (default)
    print("Example 1: Basic OTEL setup")
    setup(service_name="my-basic-service")
    
    # Example 2: OTEL setup with Gentrace samplers enabled
    print("\nExample 2: OTEL setup with Gentrace samplers")
    setup(
        service_name="my-gentrace-service",
        use_gentrace_samplers=True,
    )
    
    # Example 3: Full configuration with all options
    print("\nExample 3: Full configuration")
    setup(
        service_name="my-advanced-service",
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL"),
        use_gentrace_samplers=True,
        use_console_exporter=True,  # Useful for debugging
        extra_resource_attributes={
            "environment": "production",
            "version": "1.0.0",
            "team": "platform",
        }
    )
    
    # Now you can use OpenTelemetry as normal
    tracer = trace.get_tracer(__name__)
    
    # Example usage with interaction decorator
    @interaction(name="greeting")
    def greet(name: str) -> str:
        with tracer.start_as_current_span("format_greeting"):
            return f"Hello, {name}!"
    
    # Test the instrumented function
    result = greet("World")
    print(f"\nResult: {result}")
    
    # Example with manual span creation
    with tracer.start_as_current_span("manual_operation") as span:
        span.set_attribute("operation.type", "example")
        span.add_event("Starting operation")
        # Your operation here
        span.add_event("Operation completed")
    
    print("\nOpenTelemetry setup complete! Spans are being sent to Gentrace.")


if __name__ == "__main__":
    main()