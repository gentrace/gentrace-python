"""
Example showing different ways to configure OpenTelemetry through Gentrace init().

This demonstrates the flexibility of the auto_configure_otel parameter.
"""

import os
from typing import Any, List

import gentrace
from gentrace import GentraceSampler, OtelConfigOptions, interaction

# Optional instrumentations - these are not required dependencies
try:
    from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor  # type: ignore
    from opentelemetry.instrumentation.requests import RequestsInstrumentor  # type: ignore
    instrumentations_available = True
except ImportError:
    instrumentations_available = False

# Pipeline ID for examples
PIPELINE_ID = os.getenv("GENTRACE_PIPELINE_ID", "26d64c23-e38c-56fd-9b45-9adc87de797b")


def example_default_config() -> None:
    """Example 1: Default configuration (most common)"""
    print("\n=== Example 1: Default Configuration ===")
    
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
        # auto_configure_otel=True is the default, shown for clarity
        auto_configure_otel=True
    )
    
    print("OpenTelemetry configured with defaults:")
    print("- Service name auto-detected from pyproject.toml")
    print("- Standard sampling behavior")
    print("- Traces sent to Gentrace endpoint")


def example_custom_config() -> None:
    """Example 2: Custom configuration with options"""
    print("\n=== Example 2: Custom Configuration ===")
    
    # Using TypedDict for better type safety
    config: OtelConfigOptions = {
        "service_name": "my-custom-service",
        "debug": True,  # Enable console output for debugging
        "sampler": GentraceSampler(),  # Use Gentrace sampler for filtering
        "resource_attributes": {
            "environment": "staging",
            "version": "2.0.0"
        }
    }
    
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
        auto_configure_otel=config
    )
    
    print("OpenTelemetry configured with custom options:")
    print("- Custom service name: my-custom-service")
    print("- Debug mode enabled (console output)")
    print("- GentraceSampler for span filtering")
    print("- Additional resource attributes")


def example_with_instrumentations() -> None:
    """Example 3: Configuration with instrumentations"""
    print("\n=== Example 3: With Instrumentations ===")
    
    if not instrumentations_available:
        print("Instrumentation libraries not available.")
        print("Install them with: pip install opentelemetry-instrumentation-requests opentelemetry-instrumentation-urllib3")
        return
    
    instrumentations: List[Any] = [  # type: ignore
        RequestsInstrumentor(),  # type: ignore
        URLLib3Instrumentor(),  # type: ignore
    ]
    
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
        auto_configure_otel={
            "service_name": "instrumented-service",
            "instrumentations": instrumentations
        }
    )
    
    print("OpenTelemetry configured with instrumentations:")
    print("- Automatic tracing for requests library")
    print("- Automatic tracing for urllib3")
    
    # Now HTTP requests will be automatically traced
    @interaction(name="fetch_data", pipeline_id=PIPELINE_ID)
    def fetch_example() -> None:
        try:
            import requests
            response = requests.get("https://api.github.com")
            print(f"GitHub API status: {response.status_code}")
        except ImportError:
            print("requests library not installed")
    
    fetch_example()


def example_disabled_config() -> None:
    """Example 4: Disabled OpenTelemetry configuration"""
    print("\n=== Example 4: Disabled Configuration ===")
    
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
        auto_configure_otel=False
    )
    
    print("Gentrace initialized without OpenTelemetry")
    print("You can configure OpenTelemetry manually later")


def main() -> None:
    print("Gentrace init() Configuration Examples")
    print("=====================================")
    
    # Run different examples
    # Note: In a real application, you would only call init() once
    
    example_default_config()
    # example_custom_config()
    # example_with_instrumentations()
    # example_disabled_config()
    
    print("\n✓ Configuration complete!")
    print("Check your Gentrace dashboard for traces.")


if __name__ == "__main__":
    main()