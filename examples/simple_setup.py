"""
Simple example demonstrating the easiest way to use Gentrace with OpenTelemetry.

This example shows how the new setup() function eliminates all boilerplate code.
"""

import os

from opentelemetry import trace

import gentrace
from gentrace import setup, interaction

# Pipeline ID for this example
PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "26d64c23-e38c-56fd-9b45-9adc87de797b")


async def main() -> None:
    # Step 1: Initialize Gentrace first
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
    )
    
    # Step 2: Setup OpenTelemetry - no parameters needed!
    setup()
    
    # That's it! OpenTelemetry is now configured with:
    # - Service name auto-detected from pyproject.toml
    # - Gentrace samplers enabled by default
    # - Traces sent to Gentrace endpoint
    # - Automatic span flushing on exit
    
    # Now you can use Gentrace as normal
    tracer = trace.get_tracer(__name__)
    
    # Example 1: Using interaction decorator
    @interaction(name="greet_user", pipeline_id=PIPELINE_ID)
    async def greet(name: str) -> str:
        return f"Hello, {name}! Welcome to Gentrace."
    
    # Example 2: Manual span creation
    with tracer.start_as_current_span("manual_operation") as span:
        span.set_attribute("operation.type", "demo")
        result = await greet("World")
        span.set_attribute("result.length", len(result))
    
    print(f"Result: {result}")
    
    # Example 3: Show what happens with debug mode
    # Note: In a real app, you would only call setup() once
    print("\n--- Debug Mode Example (would be in a separate run) ---")
    print("To enable debug mode, you would use:")
    print('setup(debug=True)')
    
    print("\nSetup complete! Traces are being sent to Gentrace.")
    
    # Give time for spans to be exported
    import time
    time.sleep(2)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
