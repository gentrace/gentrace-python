import os
import sys
import json
import atexit
from typing import Any, Dict, List, Optional
from pathlib import Path

from rich.text import Text
from rich.panel import Panel
from rich.syntax import Syntax
from rich.console import Group
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.sdk.trace.sampling import Sampler

from .utils import get_console, display_gentrace_warning
from .warnings import GentraceWarnings
from .span_processor import GentraceSpanProcessor
from .client_instance import _get_sync_client_instance
from .custom_otlp_exporter import GentraceOTLPSpanExporter


def _display_init_error() -> None:
    """Display initialization error using rich formatting."""
    console = get_console()

    # Code example for fixing the error
    code_example = """from gentrace import init, setup

# First, initialize Gentrace with your API key
init(
    api_key=os.getenv('GENTRACE_API_KEY') or 'your-api-key',
    base_url='https://gentrace.ai/api',  # optional
)

# Then setup OpenTelemetry
setup()"""

    # Create error content with rich formatting
    error_content = Group(
        Text("The setup() function was called before init().", style="red"),
        Text("Gentrace must be initialized with your API key before setting up OpenTelemetry.", style="red"),
        Text(),
        Text("To fix this, call init() before setup():", style="yellow"),
    )

    # Create error panel
    error_panel = Panel(
        error_content,
        title="[red]⚠ Gentrace Initialization Error[/red]",
        border_style="red",
        title_align="left",
        padding=(1, 2),
    )

    # Display the error panel
    console.console.print(error_panel)
    console.console.print()  # Add spacing

    # Display the code example
    console.console.print(Text("Here's how to fix it:", style="bold cyan"))
    console.console.print()

    syntax = Syntax(
        code_example,
        "python",
        theme="monokai",
        line_numbers=True,
        word_wrap=True,
        background_color="default",
    )
    console.console.print(syntax)
    console.console.print()

    console.console.print(Text("💡 Make sure to call init() before setup() in your application.", style="bold green"))


def _get_service_name() -> str:
    """Auto-detect service name from pyproject.toml or setup.py."""
    # Try pyproject.toml first
    try:
        pyproject_path = Path.cwd() / "pyproject.toml"
        if pyproject_path.exists():
            # Use proper TOML parser
            try:
                # Python 3.11+ has tomllib built-in
                import tomllib  # type: ignore[import]
            except ImportError:
                # For older Python versions, use tomli
                import tomli as tomllib  # type: ignore[import, no-redef]

            with open(pyproject_path, "rb") as f:
                data: Dict[str, Any] = tomllib.load(f)  # type: ignore[attr-defined]

            # Check for project.name (PEP 621)
            if "project" in data and "name" in data["project"]:
                name = data["project"]["name"]  # type: ignore[assignment]
                if isinstance(name, str):
                    return name

            # Check for tool.poetry.name (Poetry)
            if "tool" in data and "poetry" in data["tool"] and "name" in data["tool"]["poetry"]:
                name = data["tool"]["poetry"]["name"]  # type: ignore[assignment]
                if isinstance(name, str):
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
                if "name" in data:
                    return str(data["name"])
    except Exception:
        pass

    return "unknown-service"


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
        instrumentations: Optional list of OpenTelemetry instrumentations to configure.
                         Each instrumentation should be an instance with an 'instrument' method.
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
        init(api_key="your-api-key")

        # Then setup OpenTelemetry - no parameters needed
        setup()

        # With custom trace endpoint
        setup(trace_endpoint="http://localhost:4318/v1/traces")

        # With instrumentations (Python style)
        from opentelemetry.instrumentation.requests import RequestsInstrumentation
        from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentation

        setup(
            instrumentations=[
                RequestsInstrumentation(),
                URLLib3Instrumentation(),
            ]
        )

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
        is_initialized = client and hasattr(client, "api_key") and client.api_key and client.api_key != "placeholder"

        # Also check for the global flag set by init()
        gentrace_module = sys.modules.get("gentrace")
        if not is_initialized or not (gentrace_module and getattr(gentrace_module, "__gentrace_initialized", False)):
            raise ValueError("Gentrace not initialized")

    except Exception as e:
        # Display error using rich formatting
        _display_init_error()
        raise RuntimeError("Gentrace must be initialized before calling setup().") from e

    # Get configuration values with smart defaults
    # Use API key from init() with higher priority than env variable
    api_key = client.api_key if client.api_key != "placeholder" else os.getenv("GENTRACE_API_KEY")
    base_url_obj = getattr(client, "base_url", None)

    # Convert URL object to string if needed
    if base_url_obj:
        base_url = str(base_url_obj)
    else:
        base_url = os.getenv("GENTRACE_BASE_URL", "https://gentrace.ai/api")

    # Build the trace endpoint URL
    # Ensure base_url doesn't end with a slash to avoid double slashes
    base_url_clean = base_url.rstrip("/")
    final_trace_endpoint = trace_endpoint or f"{base_url_clean}/otel/v1/traces"

    # Get service name with auto-detection
    final_service_name = service_name or _get_service_name()

    # Build resource attributes
    all_resource_attributes = {"service.name": final_service_name, **(resource_attributes or {})}

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
        warning = GentraceWarnings.MissingApiKeyError()
        display_gentrace_warning(warning)
        raise ValueError(
            "GENTRACE_API_KEY is required when using Gentrace endpoint. "
            "Please set the GENTRACE_API_KEY environment variable or call init() with an API key."
        )

    # Create custom OTLP exporter with partial success handling
    otlp_exporter = GentraceOTLPSpanExporter(
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
            console = get_console()
            console.error(f"Error during OpenTelemetry shutdown: {e}")

    # Register for different exit scenarios
    atexit.register(shutdown_handler)

    # Configure instrumentations if provided
    # Standard pattern is to pass instances: RequestsInstrumentor().instrument()
    if instrumentations:
        for instrumentation in instrumentations:
            try:
                # All standard OpenTelemetry instrumentations inherit from BaseInstrumentor
                # which provides the instrument() method
                if hasattr(instrumentation, "instrument") and callable(instrumentation.instrument):
                    # Check if this is an OpenInference instrumentor which needs tracer_provider
                    # OpenInference instrumentors are in the openinference.instrumentation namespace
                    module_name = type(instrumentation).__module__
                    if module_name and "openinference.instrumentation" in module_name:
                        # OpenInference instrumentors need the tracer_provider
                        instrumentation.instrument(tracer_provider=tracer_provider)
                    else:
                        # Standard OpenTelemetry instrumentors
                        instrumentation.instrument()
                else:
                    import warnings

                    warnings.warn(
                        f"Instrumentation {type(instrumentation).__name__} does not have an 'instrument' method. "
                        f"Ensure you're passing an instance, not a class.",
                        UserWarning,
                        stacklevel=2,
                    )
            except Exception as e:
                import warnings

                warnings.warn(
                    f"Failed to configure instrumentation {type(instrumentation).__name__}: {e}",
                    UserWarning,
                    stacklevel=2,
                )

    return tracer_provider


__all__ = ["setup"]
