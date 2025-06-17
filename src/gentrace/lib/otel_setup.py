import os
import sys
import json
import atexit
from typing import Any, Dict, List, Optional
from pathlib import Path

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.sdk.trace.sampling import Sampler
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from .sampler import GentraceSampler
from .span_processor import GentraceSpanProcessor
from .client_instance import _get_sync_client_instance


def _format_error_message() -> str:
    """Format error message with colors if terminal supports it."""
    # Check if we're in a terminal that supports colors
    supports_color = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    if supports_color:
        # ANSI color codes
        red = '\033[91m'
        cyan = '\033[96m'
        gray = '\033[90m'
        reset = '\033[0m'
        bold = '\033[1m'
    else:
        red = cyan = gray = reset = bold = ''
    
    title = f"{red}{bold}⚠ Gentrace Initialization Error{reset}"
    
    message = f"""
{title}

The setup() function was called before init(). Gentrace must be initialized
with your API key before setting up OpenTelemetry.

To fix this, call init() before setup():

{cyan}from gentrace import init, setup

# First, initialize Gentrace with your API key
init(
    api_key=os.getenv('GENTRACE_API_KEY') or 'your-api-key',
    base_url='https://gentrace.ai/api',  # optional
)

# Then setup OpenTelemetry
setup(){reset}

{gray}Make sure to call init() before setup() in your application.{reset}
"""
    return message


def _get_service_name() -> str:
    """Auto-detect service name from pyproject.toml or setup.py."""
    # Try pyproject.toml first
    try:
        pyproject_path = Path.cwd() / "pyproject.toml"
        if pyproject_path.exists():
            # Simple TOML parsing for the name field
            content = pyproject_path.read_text()
            for line in content.split('\n'):
                if line.strip().startswith('name'):
                    # Extract value between quotes
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        name = parts[1].strip().strip('"').strip("'")
                        if name:
                            return name
    except Exception:
        pass
    
    # Try setup.py
    try:
        setup_path = Path.cwd() / "setup.py"
        if setup_path.exists():
            # Look for name= in setup()
            content = setup_path.read_text()
            import re
            match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                return match.group(1)
    except Exception:
        pass
    
    # Try package.json for Node.js projects using Python
    try:
        package_json_path = Path.cwd() / "package.json"
        if package_json_path.exists():
            with open(package_json_path) as f:
                data = json.load(f)
                if 'name' in data:
                    return str(data['name'])
    except Exception:
        pass
    
    return 'unknown-service'


def setup(
    *,
    trace_endpoint: Optional[str] = None,
    service_name: Optional[str] = None,
    instrumentations: Optional[List[Any]] = None,
    resource_attributes: Optional[Dict[str, Any]] = None,
    sampler: Optional[Sampler] = None,
    debug: bool = False,
) -> TracerProvider:
    """
    Sets up OpenTelemetry with Gentrace configuration.
    
    This is the simplest way to initialize OpenTelemetry for use with Gentrace.
    By default, it configures everything needed to send traces to Gentrace.
    
    The setup function automatically registers process exit handlers to ensure
    spans are properly flushed when the process exits.
    
    IMPORTANT: You must call init() before setup() to initialize Gentrace with your API key.
    
    Args:
        trace_endpoint: Optional OpenTelemetry trace endpoint URL.
                       Defaults to Gentrace's OTLP endpoint.
        service_name: Optional service name for the application.
                     Defaults to the package name from pyproject.toml or 'unknown-service'.
        instrumentations: Optional instrumentations to include (e.g., OpenAI, Anthropic).
        resource_attributes: Optional additional resource attributes.
        sampler: Optional custom sampler. If not provided, uses OpenTelemetry's default
                 sampling behavior. Use GentraceSampler() to filter spans based on
                 gentrace.sample attribute.
        debug: Whether to include console exporter for debugging (defaults to False).
        
    Returns:
        The configured TracerProvider instance
        
    Example:
        ```python
        from gentrace import init, setup
        
        # First, initialize Gentrace
        init(api_key='your-api-key')
        
        # Then setup OpenTelemetry - no parameters needed
        setup()
        
        # With custom trace endpoint
        setup(trace_endpoint='http://localhost:4318/v1/traces')
        
        # With instrumentations
        setup(instrumentations=[OpenAIInstrumentation()])
        
        # With GentraceSampler to filter spans
        from gentrace import GentraceSampler
        setup(sampler=GentraceSampler())
        ```
    """
    # Check if init() has been called
    try:
        client = _get_sync_client_instance()
        # Check if the client has been properly initialized
        # The client should have a valid API key (not the default placeholder)
        is_initialized = (
            client and 
            hasattr(client, 'api_key') and 
            client.api_key and 
            client.api_key != 'placeholder'
        )
        
        # Also check for the global flag set by init()
        if not is_initialized or not getattr(sys.modules.get('gentrace', {}), '__gentrace_initialized', False):
            raise ValueError("Gentrace not initialized")
            
    except Exception as e:
        # Display error and exit
        sys.stderr.write(_format_error_message() + '\n')
        raise RuntimeError("Gentrace must be initialized before calling setup().") from e
    
    # Get configuration values with smart defaults
    # Use API key from init() with higher priority than env variable
    api_key = client.api_key if client.api_key != 'placeholder' else os.getenv('GENTRACE_API_KEY')
    base_url_obj = getattr(client, 'base_url', None)
    
    # Convert URL object to string if needed
    if base_url_obj:
        base_url = str(base_url_obj)
    else:
        base_url = os.getenv('GENTRACE_BASE_URL', 'https://gentrace.ai/api')
    
    # Build the trace endpoint URL
    final_trace_endpoint = trace_endpoint or f"{base_url}/otel/v1/traces"
    
    # Get service name with auto-detection
    final_service_name = service_name or _get_service_name()
    
    # Build resource attributes
    all_resource_attributes = {
        "service.name": final_service_name,
        **(resource_attributes or {})
    }
    
    # Create resource
    resource = Resource(attributes=all_resource_attributes)
    
    # Create the tracer provider with sampler only if explicitly provided
    if sampler:
        tracer_provider = TracerProvider(resource=resource, sampler=sampler)
    else:
        # No sampler specified - use OpenTelemetry's default behavior
        tracer_provider = TracerProvider(resource=resource)
    
    # Setup span processors
    # Always add GentraceSpanProcessor for baggage enrichment
    gentrace_processor = GentraceSpanProcessor()
    tracer_provider.add_span_processor(gentrace_processor)
    
    # Configure trace exporter
    exporter_headers: Dict[str, str] = {
        "Content-Type": "application/json",
    }
    
    # Add authorization header if we have an API key
    if api_key:
        exporter_headers["Authorization"] = f"Bearer {api_key}"
    elif not trace_endpoint:
        # Only throw error if using default Gentrace endpoint without API key
        raise ValueError(
            "GENTRACE_API_KEY is required when using Gentrace endpoint. "
            "Please set the GENTRACE_API_KEY environment variable or call init() with an API key."
        )
    
    # Create OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=final_trace_endpoint,
        headers=exporter_headers,
    )
    
    # Add main export processor
    export_processor = SimpleSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(export_processor)
    
    # Add console exporter if debug mode
    if debug:
        console_processor = SimpleSpanProcessor(ConsoleSpanExporter())
        tracer_provider.add_span_processor(console_processor)
    
    # Set as global tracer provider
    trace.set_tracer_provider(tracer_provider)
    
    # Register shutdown handlers
    def shutdown_handler() -> None:
        try:
            tracer_provider.shutdown()
        except Exception as e:
            sys.stderr.write(f"Error during OpenTelemetry shutdown: {e}\n")
    
    # Register for different exit scenarios
    atexit.register(shutdown_handler)
    
    # Note: instrumentations are not directly supported by Python's TracerProvider
    # Users should configure instrumentations separately if needed
    if instrumentations:
        import warnings
        warnings.warn(
            "The 'instrumentations' parameter is not directly supported in Python. "
            "Please configure instrumentations separately.",
            UserWarning,
            stacklevel=2
        )
    
    return tracer_provider


__all__ = ["setup"]