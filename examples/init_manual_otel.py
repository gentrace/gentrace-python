"""
Example showing how to initialize Gentrace without automatic OpenTelemetry configuration.

This is useful when:
1. You want to configure OpenTelemetry manually with custom settings
2. You're integrating with an existing OpenTelemetry setup
3. You want to delay OpenTelemetry configuration
"""

import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

import gentrace
from gentrace import GentraceSpanProcessor


def main() -> None:
    # Initialize Gentrace WITHOUT automatic OpenTelemetry configuration
    gentrace.init(
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

    # Now you can use tracing as normal
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("manual_config_test") as span:
        span.set_attribute("config.type", "manual")
        print("Created test span with manual configuration")


if __name__ == "__main__":
    main()
