"""
Example showing how to initialize Gentrace without automatic OpenTelemetry configuration.

This is useful when:
1. You want to configure OpenTelemetry manually with custom settings
2. You're integrating with an existing OpenTelemetry setup
3. You want to delay OpenTelemetry configuration

This example demonstrates creating spans with gentrace.pipeline_id attributes
for proper Gentrace interaction tracking.
"""

import os
import json

from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from gentrace import GentraceSpanProcessor, init

load_dotenv()


def main() -> None:
    # Initialize Gentrace WITHOUT automatic OpenTelemetry configuration
    init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        base_url=os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api"),
        otel_setup=False,  # Disable automatic OpenTelemetry setup
    )

    print("Gentrace initialized without OpenTelemetry")

    # Now you can configure OpenTelemetry manually with custom settings
    # For example, with a custom resource and multiple exporters
    resource = Resource(
        attributes={"service.name": "my-custom-service", "service.version": "1.0.0", "environment": "production"}
    )

    tracer_provider = TracerProvider(resource=resource)

    # Add Gentrace span processor for baggage enrichment
    gentrace_processor = GentraceSpanProcessor()
    tracer_provider.add_span_processor(gentrace_processor)

    # Configure OTLP exporter with custom endpoint
    otlp_exporter = OTLPSpanExporter(
        endpoint=f"{os.getenv('GENTRACE_BASE_URL', 'https://gentrace.ai/api')}/otel/v1/traces",
        headers={"Authorization": f"Bearer {os.getenv('GENTRACE_API_KEY')}"},
    )
    tracer_provider.add_span_processor(SimpleSpanProcessor(otlp_exporter))

    # Set the tracer provider
    trace.set_tracer_provider(tracer_provider)

    print("Custom OpenTelemetry configuration complete!")

    # Get pipeline ID for Gentrace interaction tracking
    pipeline_id = os.getenv("GENTRACE_PIPELINE_ID")
    if not pipeline_id:
        print("Warning: GENTRACE_PIPELINE_ID not set. Creating span without pipeline association.")
        pipeline_id = ""

    # Create a span with gentrace.pipeline_id attribute for proper Gentrace interaction tracking
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("manual_config_test") as span:

        # Set Gentrace-specific attributes for interaction/traced spans
        span.set_attribute("gentrace.pipeline_id", pipeline_id)
        span.set_attribute("gentrace.sample", "true")
        span.set_attribute("config.type", "manual")
        
        # Add gentrace.fn.args event - marks function invocation with input arguments
        function_args = ["test_input", {"config": "manual"}]
        span.add_event(
            "gentrace.fn.args",
            attributes={"args": json.dumps(function_args)}
        )
        
        print(f"Created test span with manual configuration and gentrace.pipeline_id: {pipeline_id}")
        print("This span will be tracked as a Gentrace interaction span")
        
        # Simulate some work
        result = {"status": "success", "message": "Manual OpenTelemetry configuration test completed"}
        
        # Add gentrace.fn.output event - marks successful function completion with output
        span.add_event(
            "gentrace.fn.output",
            attributes={"output": json.dumps(result)}
        )
        
        print(f"Function completed with result: {result}")
        print("Added gentrace.fn.args and gentrace.fn.output events to span")


if __name__ == "__main__":
    main()
