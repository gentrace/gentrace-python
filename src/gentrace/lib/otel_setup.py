import atexit
import os
from typing import Dict, Optional, List
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.sampling import Sampler, AlwaysOnSampler

from .sampler import GentraceSampler
from .span_processor import GentraceSpanProcessor


def setup(
    *,
    service_name: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    use_gentrace_samplers: bool = False,
    extra_processors: Optional[List[SpanProcessor]] = None,
    extra_resource_attributes: Optional[Dict[str, str]] = None,
    use_console_exporter: bool = False,
    custom_sampler: Optional[Sampler] = None,
) -> TracerProvider:
    """
    Initialize OpenTelemetry with Gentrace configuration.
    
    This function sets up the OpenTelemetry tracer provider with sensible defaults
    for use with Gentrace, handling all the boilerplate setup.
    
    Args:
        service_name: The name of your service/application
        api_key: Gentrace API key. If not provided, uses GENTRACE_API_KEY env var
        base_url: Gentrace base URL. If not provided, uses GENTRACE_BASE_URL env var 
                  or defaults to https://api.gentrace.ai
        use_gentrace_samplers: Whether to use GentraceSampler. Defaults to False
        extra_processors: Additional span processors to add
        extra_resource_attributes: Additional resource attributes to include
        use_console_exporter: Whether to also export spans to console (useful for debugging)
        custom_sampler: Custom sampler to use instead of default samplers
        
    Returns:
        The configured TracerProvider instance
        
    Example:
        ```python
        from gentrace import setup
        
        # Basic usage
        setup(service_name="my-service")
        
        # With Gentrace samplers
        setup(service_name="my-service", use_gentrace_samplers=True)
        
        # With additional configuration
        setup(
            service_name="my-service",
            api_key="your-api-key",
            use_gentrace_samplers=True,
            use_console_exporter=True,
            extra_resource_attributes={"environment": "production"}
        )
        ```
    """
    # Get API key and base URL from environment if not provided
    if api_key is None:
        api_key = os.getenv("GENTRACE_API_KEY")
    
    if base_url is None:
        base_url = os.getenv("GENTRACE_BASE_URL", "https://api.gentrace.ai")
    
    # Create resource with service name and any extra attributes
    resource_attributes = {"service.name": service_name}
    if extra_resource_attributes:
        resource_attributes.update(extra_resource_attributes)
    resource = Resource(attributes=resource_attributes)
    
    # Determine which sampler to use
    if custom_sampler:
        sampler = custom_sampler
    elif use_gentrace_samplers:
        sampler = GentraceSampler()
    else:
        sampler = AlwaysOnSampler()
    
    # Create the tracer provider
    tracer_provider = TracerProvider(resource=resource, sampler=sampler)
    
    # Configure OTLP headers for authentication
    otlp_headers: Dict[str, str] = {}
    if api_key:
        otlp_headers["Authorization"] = f"Bearer {api_key}"
    
    # Create OTLP span exporter
    span_exporter = OTLPSpanExporter(
        endpoint=f"{base_url}/otel/v1/traces",
        headers=otlp_headers,
    )
    
    # Add processors
    # Always add GentraceSpanProcessor for baggage enrichment when using Gentrace samplers
    if use_gentrace_samplers:
        gentrace_baggage_processor = GentraceSpanProcessor()
        tracer_provider.add_span_processor(gentrace_baggage_processor)
    
    # Add the main export processor
    simple_export_processor = SimpleSpanProcessor(span_exporter)
    tracer_provider.add_span_processor(simple_export_processor)
    
    # Add console exporter if requested
    if use_console_exporter:
        console_processor = SimpleSpanProcessor(ConsoleSpanExporter())
        tracer_provider.add_span_processor(console_processor)
    
    # Add any extra processors
    if extra_processors:
        for processor in extra_processors:
            tracer_provider.add_span_processor(processor)
    
    # Set as global tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    # Register shutdown handler to ensure spans are flushed on exit
    atexit.register(tracer_provider.shutdown)
    
    return tracer_provider


__all__ = ["setup"]