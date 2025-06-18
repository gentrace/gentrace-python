"""
Example demonstrating the typed interface for OpenTelemetry configuration.

This shows how OtelConfigOptions provides better IDE support and type safety.
"""

import os

from gentrace import GentraceSampler, OtelConfigOptions, init


def main() -> None:
    # Example 1: Using the typed configuration directly
    # IDEs will provide autocomplete for all available options
    otel_config: OtelConfigOptions = {
        "service_name": "my-typed-service",
        "debug": True,
        "sampler": GentraceSampler(),
        "resource_attributes": {
            "environment": "production",
            "version": "1.0.0",
            "team": "backend"
        }
    }
    
    init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
        otel_setup=otel_config
    )
    
    print("✓ Gentrace initialized with typed OpenTelemetry configuration")
    print(f"  Service: {otel_config['service_name']}")
    print(f"  Debug mode: {otel_config['debug']}")
    print(f"  Using GentraceSampler: {'sampler' in otel_config}")
    
    # Example 2: Inline configuration also benefits from type hints
    # Your IDE should provide autocomplete for the dictionary keys
    # init(
    #     api_key="...",
    #     otel_setup={
    #         "service_name": "inline-service",  # IDE autocomplete works here!
    #         "debug": False,
    #         "trace_endpoint": "http://custom-endpoint:4318/v1/traces"
    #     }
    # )


if __name__ == "__main__":
    main()