"""Example demonstrating Gentrace's automatic AST-based tracing with pipeline_id support.

This example shows how auto-traced functions can be associated with a specific
Gentrace pipeline and exported to the Gentrace backend.

To run this example, ensure the following environment variables are set:
    GENTRACE_API_KEY: Your Gentrace API token for authentication.
    GENTRACE_BASE_URL: The base URL for your Gentrace instance (e.g., http://localhost:3000/api).
    GENTRACE_PIPELINE_ID: The UUID of the pipeline to associate traces with.
    OPENAI_API_KEY: Your OpenAI API key (optional, for OpenAI examples).
"""

import os
import atexit
from typing import Dict

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

import gentrace
from gentrace import GentraceSampler, GentraceSpanProcessor

# Get configuration from environment
api_key = os.getenv("GENTRACE_API_KEY", "")
gentrace_base_url = os.getenv("GENTRACE_BASE_URL", "")
pipeline_id = os.getenv("GENTRACE_PIPELINE_ID", "")

if not api_key:
    raise ValueError("GENTRACE_API_KEY environment variable not set.")
if not gentrace_base_url:
    raise ValueError("GENTRACE_BASE_URL environment variable not set.")
if not pipeline_id:
    raise ValueError("GENTRACE_PIPELINE_ID environment variable not set.")

print(f"Gentrace Base URL: {gentrace_base_url}")
print(f"Pipeline ID: {pipeline_id}")
print("=" * 60)

# Setup OpenTelemetry with Gentrace
resource = Resource(attributes={"service.name": "auto-trace-pipeline-example"})
tracer_provider = TracerProvider(resource=resource, sampler=GentraceSampler())

# Configure OTLP exporter to send traces to Gentrace
otlp_headers: Dict[str, str] = {}
if api_key:
    otlp_headers["Authorization"] = f"Bearer {api_key}"

span_exporter = OTLPSpanExporter(
    endpoint=f"{gentrace_base_url}/otel/v1/traces",
    headers=otlp_headers,
)

# Add Gentrace span processor for enrichment
gentrace_baggage_processor = GentraceSpanProcessor()
tracer_provider.add_span_processor(gentrace_baggage_processor)

# Add the export processor
simple_export_processor = SimpleSpanProcessor(span_exporter)
tracer_provider.add_span_processor(simple_export_processor)

# Set the global tracer provider
trace.set_tracer_provider(tracer_provider)

# Install auto-tracing with pipeline_id for our example modules
# All functions in these modules will be automatically associated with this pipeline
print("Installing auto-tracing with pipeline_id...")
gentrace.install_auto_tracing(
    ['pipeline_example_app'],
    min_duration=0,
    pipeline_id=pipeline_id
)

# Now import the modules - they will be automatically instrumented with pipeline_id
from pipeline_example_app import workflow

if __name__ == "__main__":
    # Register shutdown handler
    atexit.register(tracer_provider.shutdown)
    
    print("\nStarting Gentrace Auto-Trace Pipeline Example")
    print("=" * 60)
    
    # Run the workflow - all traced functions will include the pipeline_id
    try:
        result = workflow.run_data_processing_pipeline()
        
        print("\n" + "=" * 60)
        print(f"Pipeline completed successfully!")
        print(f"Result: {result}")
        print(f"\nMost spans include 'gentrace.pipeline_id': '{pipeline_id}'")
        print("Note: The 'enrich_summary_manually' function uses @traced decorator")
        print("to demonstrate manual tracing within auto-traced code.")
        print("\nCheck the Gentrace dashboard to see the mixed trace!")
    except Exception as e:
        print(f"\nError running pipeline: {e}")
        raise
    
    print("\nShutting down...")
    # Force flush to ensure all spans are sent
    tracer_provider.force_flush()
    
    # Add a small delay to ensure spans are processed
    import time
    time.sleep(1)