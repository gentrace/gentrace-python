"""
This example demonstrates what happens when using Gentrace's @interaction decorator
without setting up OpenTelemetry first. This will show warning/error messages about
missing OpenTelemetry configuration.
"""

import os
import asyncio

from gentrace import interaction

api_key = os.getenv("GENTRACE_API_KEY", "")
pipeline_id = os.getenv("GENTRACE_PIPELINE_ID", "")

if not api_key:
    print("Warning: GENTRACE_API_KEY environment variable not set.")


@interaction(pipeline_id=pipeline_id, name="test_sync_interaction")
def my_sync_function(x: int, y: int) -> int:
    result = x + y
    print(f"Sync function executed: {x} + {y} = {result}")
    return result


@interaction(pipeline_id=pipeline_id, name="test_async_interaction")
async def my_async_function(message: str) -> str:
    await asyncio.sleep(0.1)
    result = f"Processed: {message}"
    print(f"Async function executed: {result}")
    return result


async def main() -> None:
    print("Running Gentrace interactions without OpenTelemetry setup...\n")
    
    print("=== Testing synchronous interaction ===")
    try:
        sync_result = my_sync_function(5, 3)
        print(f"Sync result: {sync_result}\n")
    except Exception as e:
        print(f"Error in sync function: {e}\n")
    
    print("=== Testing asynchronous interaction ===")
    try:
        async_result = await my_async_function("Hello Gentrace")
        print(f"Async result: {async_result}\n")
    except Exception as e:
        print(f"Error in async function: {e}\n")
    
    print("\nNote: Check console output above for any warnings about missing OpenTelemetry configuration.")


if __name__ == "__main__":
    asyncio.run(main()) 