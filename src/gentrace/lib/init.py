import traceback
from typing import Any, Dict, List, Union, Optional, cast
from datetime import datetime

from gentrace import Gentrace, AsyncGentrace

from .types import OtelConfigOptions
from .utils import generate_config_diff
from .warnings import GentraceWarnings
from .otel_setup import setup as _setup_otel
from .client_instance import _set_client_instances


# Module-level variables to track initialization history
class InitCall:
    """Record of an init() call"""
    def __init__(self, timestamp: datetime, options: Dict[str, Any], call_number: int, stack_trace: Optional[str] = None):
        self.timestamp = timestamp
        self.options = options
        self.call_number = call_number
        self.stack_trace = stack_trace


_init_history: List[InitCall] = []
_init_call_count: int = 0


def _get_init_history() -> List[InitCall]:
    """Get the initialization history"""
    return _init_history


def _add_init_call(options: Dict[str, Any]) -> InitCall:
    """Record a new init call"""
    global _init_call_count
    _init_call_count += 1
    
    # Capture stack trace for debugging
    stack = None
    try:
        stack = ''.join(traceback.format_stack()[:-1])  # Exclude this function
    except Exception:
        pass
    
    init_call = InitCall(
        timestamp=datetime.now(),
        options=options,
        call_number=_init_call_count,
        stack_trace=stack
    )
    _init_history.append(init_call)
    return init_call


def init(
    *,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    otel_setup: Union[bool, OtelConfigOptions] = True,
    **kwargs: Any,
) -> None:
    """
    Initializes the Gentrace SDK and configures OpenTelemetry by default.

    This function sets up both synchronous and asynchronous Gentrace clients,
    and automatically configures OpenTelemetry for tracing (unless disabled).

    If `api_key` is not provided, the underlying clients will attempt to use the
    GENTRACE_API_KEY environment variable. If `base_url` is not provided, they will
    attempt to use the GENTRACE_BASE_URL environment variable or a default URL.

    All arguments must be passed as keyword arguments.

    Args:
        api_key (Optional[str]): The Gentrace API key.
            If None, GENTRACE_API_KEY environment variable is used by clients.
        base_url (Optional[str]): The base URL for the Gentrace API. If not provided,
            it's determined by the client (env variable or default).
        otel_setup (Union[bool, OtelConfigOptions]): Controls OpenTelemetry configuration.
            - True (default): Automatically configures OpenTelemetry with default settings
            - False: Skips OpenTelemetry configuration
            - OtelConfigOptions: TypedDict with the following optional fields:
                - trace_endpoint: Custom OTLP endpoint URL
                - service_name: Service name (auto-detected if not provided)
                - instrumentations: List of OpenTelemetry instrumentation instances
                - resource_attributes: Additional resource attributes
                - sampler: Custom sampler (defaults to standard behavior)
                - debug: Enable console exporter for debugging (default: False)
        **kwargs (Any): Additional keyword arguments passed to the underlying
            `Gentrace` (synchronous) and `AsyncGentrace` (asynchronous)
            client constructors. This allows for advanced configuration.
            Common options include `timeout`, `max_retries`, `default_headers`,
            `default_query`, and `http_client`.

    Side Effects:
        - Sets the internal singleton client instances used by the SDK
        - Configures OpenTelemetry TracerProvider (unless otel_setup=False)
        - Registers shutdown handlers for proper span flushing

    Example:
        ```python
        from gentrace import init
        
        # Simple initialization with automatic OpenTelemetry setup
        init(api_key="your-api-key")

        # Initialize without OpenTelemetry configuration
        init(api_key="your-api-key", otel_setup=False)

        # Initialize with custom OpenTelemetry settings
        init(api_key="your-api-key", otel_setup={"service_name": "my-service", "debug": True})
        ```
    """
    # Build the complete options for comparison
    all_options: Dict[str, Any] = {}
    if api_key is not None:
        all_options["api_key"] = api_key
    if base_url is not None:
        all_options["base_url"] = base_url
    all_options["otel_setup"] = otel_setup
    all_options.update(kwargs)
    
    # Check initialization history
    init_history = _get_init_history()
    if init_history:
        # Compare with the most recent initialization
        previous_call = init_history[-1]
        diff_lines = generate_config_diff(previous_call.options, all_options)
        
        if diff_lines:
            # Only show warning if configuration actually changed
            warning = GentraceWarnings.MultipleInitWarning(
                call_number=_init_call_count + 1,
                diff_lines=diff_lines,
                init_history=[{
                    'timestamp': call.timestamp,
                    'callNumber': call.call_number
                } for call in init_history]
            )
            warning.display()
    
    # Record this initialization
    _add_init_call(all_options)
    
    # Build constructor args (without otel_setup which isn't passed to clients)
    constructor_args: Dict[str, Any] = {}
    if api_key is not None:
        constructor_args["api_key"] = api_key

    if base_url is not None:
        constructor_args["base_url"] = base_url

    constructor_args.update(kwargs)

    sync_g_client = Gentrace(**constructor_args)
    async_g_client = AsyncGentrace(**constructor_args)

    _set_client_instances(sync_g_client, async_g_client)

    # Set a global flag to indicate that init() has been called
    # Also store the otel_setup configuration
    import sys
    setattr(sys.modules["gentrace"], "__gentrace_initialized", True)
    setattr(sys.modules["gentrace"], "__gentrace_otel_setup_config", otel_setup)
    
    # Configure OpenTelemetry if requested
    if otel_setup is not False:
        # Extract OpenTelemetry configuration options
        if isinstance(otel_setup, dict):
            # Use the dict directly - it could be OtelConfigOptions or a plain dict
            otel_config = cast(Dict[str, Any], otel_setup)
        else:
            # Default configuration
            otel_config = {}

        # Call the setup function with the configuration
        _setup_otel(**otel_config)


__all__ = ["init", "_get_init_history", "_add_init_call"]
