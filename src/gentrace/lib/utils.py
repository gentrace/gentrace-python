import json
import logging
import warnings
from typing import Any, Set, Dict

from pydantic import BaseModel
from rich.text import Text
from rich.syntax import Syntax
from rich.console import Console
from opentelemetry import trace as trace_api
from opentelemetry.util import types as otel_types
from opentelemetry.sdk.trace import TracerProvider as SDKTracerProvider

logger = logging.getLogger("gentrace")

OTLP_MAX_INT_SIZE = (2**63) - 1  # Max 64-bit signed integer
OTLP_MIN_INT_SIZE = -(2**63)  # Min 64-bit signed integer

CIRCULAR_REFERENCE_PLACEHOLDER = "[CircularReference]"

# Global flag to ensure the OpenTelemetry configuration warning is issued only once per session
_otel_config_warning_issued = False


def check_otel_config_and_warn() -> None:
    """
    Checks if a proper OpenTelemetry SDK TracerProvider is configured.
    If not, issues a warning using `rich` for hyperlink formatting and displays
    formatted OTEL starter code that can be used directly.
    The warning is issued only once per Python session.
    """
    global _otel_config_warning_issued
    if _otel_config_warning_issued:
        return

    provider = trace_api.get_tracer_provider()

    if not isinstance(provider, SDKTracerProvider):
        otel_setup_url = "https://github.com/gentrace/gentrace-python/blob/main/README.md#opentelemetry-integration"
        link_text = "Gentrace OpenTelemetry Setup Guide"

        # OTEL starter code that users can copy and use directly
        otel_starter_code = '''import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Set up the resource with service name
resource = Resource(attributes={"service.name": "your-service-name"})

# Create and set the tracer provider
trace.set_tracer_provider(TracerProvider(resource=resource))

# Configure the OTLP exporter for Gentrace
otlp_headers = {"Authorization": f"Bearer {os.getenv('GENTRACE_API_KEY')}"}
span_exporter = OTLPSpanExporter(
    endpoint=f"{os.getenv('GENTRACE_BASE_URL', 'https://gentrace.ai')}/otel/v1/traces",
    headers=otlp_headers
)

# Add the span processor
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(span_exporter))

print("OpenTelemetry SDK started – spans will be sent to Gentrace.")'''

        try:
            console = Console(stderr=True, highlight=False)
            
            # Primary warning message using rich for hyperlink support
            message = Text()
            message.append(
                "Gentrace: OpenTelemetry SDK (TracerProvider) does not appear to be configured. ", style="yellow"
            )
            message.append("Gentrace tracing features (e.g., ")
            message.append("@interaction", style="on grey30")
            message.append(", ")
            message.append("@eval", style="on grey30")
            message.append(", ")
            message.append("@traced", style="on grey30")
            message.append(", and ")
            message.append("eval_dataset()", style="on grey30")
            message.append(") may not record data. ")
            message.append("Please ensure OpenTelemetry is set up as per the ")
            message.append(link_text, style=f"underline #90EE90 link {otel_setup_url}")
            message.append(".")

            console.print(message)
            console.print()  # Add spacing
            
            # Display the formatted OTEL starter code
            console.print(Text("Here's the OTEL starter code you can use:", style="bold cyan"))
            console.print()
            
            syntax = Syntax(
                otel_starter_code,
                "python",
                theme="monokai",
                line_numbers=True,
                word_wrap=True,
                background_color="default"
            )
            console.print(syntax)
            console.print()
            
            console.print(Text("💡 Copy the code above and add it to your application startup.", style="bold green"))

        except Exception:  # Fallback if rich formatting/printing fails
            fallback_message = (
                f"Gentrace: OpenTelemetry SDK (TracerProvider) does not appear to be configured. "
                f"Gentrace tracing features (e.g., @interaction, @eval, @traced, and eval_dataset()) may not record data. "
                f"Please ensure OpenTelemetry is set up as per the {otel_setup_url}."
            )
            warnings.warn(fallback_message, UserWarning, stacklevel=2)

        _otel_config_warning_issued = True


def _convert_pydantic_model_to_dict_if_applicable(obj: Any) -> Any:
    """Checks if an object is a Pydantic model and converts it to a dict.
    Returns the original object if it's not a Pydantic model or conversion fails.
    """
    if isinstance(obj, BaseModel):
        try:
            # Pydantic V2
            return obj.model_dump()
        except AttributeError:
            # Pydantic V1
            try:
                return obj.dict()  # type: ignore
            except AttributeError:
                # Should not happen if isinstance check passed and it's a Pydantic model
                pass  # Fall through, returning original obj
    return obj


def _gentrace_json_dumps(value: Any) -> str:
    """Helper to dump objects to JSON string, handling circular references and non-serializable types.

    This is a serialization function designed to help properly convert Open Telemetry span attributes
    or convert the function arguments and outputs to a serializable format.
    """

    # Attempt to convert top-level value if it's a Pydantic model
    value = _convert_pydantic_model_to_dict_if_applicable(value)

    seen_objects_for_this_dump: Set[int] = set()

    def default_handler(obj: Any) -> Any:
        obj_id = id(obj)
        if obj_id in seen_objects_for_this_dump:
            return CIRCULAR_REFERENCE_PLACEHOLDER

        seen_objects_for_this_dump.add(obj_id)

        # Attempt to convert Pydantic models to dict
        # Must be done before trying str(obj) as Pydantic models might have custom __str__
        processed_obj = _convert_pydantic_model_to_dict_if_applicable(obj)

        # If the object was a Pydantic model and successfully converted,
        # processed_obj will be a dict. Otherwise, it's the original obj.
        # We only proceed to str(obj) if it wasn't a Pydantic model or conversion failed.
        if processed_obj is not obj:  # Check if conversion happened
            # If it was converted (e.g. to a dict), it's ready for json.dumps
            return processed_obj

        try:
            return str(obj)
        except Exception:
            return f"[UnserializableType: {type(obj).__name__}]"

    try:
        return json.dumps(value, default=default_handler)
    except ValueError as e:
        if "Circular reference detected" in str(e):
            # This case should ideally be caught by the default_handler.
            # If it still occurs, it means a very complex or deep cycle was not fully handled before json.dumps itself gave up.
            # We return a simple placeholder for the entire problematic value.
            # To be more granular, the default_handler would need to be even more sophisticated
            # or we'd need a pre-processing step to replace cycles before calling json.dumps.
            warnings.warn(
                f"Fallback to placeholder for entire value due to complex circular reference: {e}",
                UserWarning,
                stacklevel=2,
            )
            return json.dumps(CIRCULAR_REFERENCE_PLACEHOLDER)
        raise  # Re-raise other ValueErrors
    except TypeError as e:
        # Fallback if default_handler somehow returns a type json.dumps still can't handle,
        # or if the initial `value` itself is problematic in a way that bypasses the default logic early.
        warnings.warn(
            f"Fallback JSON serialization due to TypeError: {e}. Result may be lossy.", UserWarning, stacklevel=2
        )
        # Final fallback to simple str conversion for the whole object if custom logic fails.
        return json.dumps(str(value), default=str)


def gentrace_format_otel_value(value: Any) -> otel_types.AttributeValue:
    """Convert a user attribute value to an OpenTelemetry compatible type.

    Simple types (str, bool, float) are passed through.
    Integers are checked against OTel's 64-bit range and converted to string if outside.
    All other types (lists, dicts, complex objects) are JSON stringified using a safe dumper.
    """
    if isinstance(value, (str, bool, float)):
        return value
    elif isinstance(value, int):
        if not (OTLP_MIN_INT_SIZE <= value <= OTLP_MAX_INT_SIZE):
            warnings.warn(
                f"Integer value {value} is outside the OTLP 64-bit signed integer range "
                f"({OTLP_MIN_INT_SIZE} to {OTLP_MAX_INT_SIZE}), it will be converted to a string.",
                UserWarning,
                stacklevel=2,
            )
            return str(value)
        return value
    else:
        # For lists, dicts, complex objects, etc., JSON stringify safely.
        return _gentrace_json_dumps(value)


def gentrace_format_otel_attributes(attributes: Dict[str, Any]) -> Dict[str, otel_types.AttributeValue]:
    """Prepare an attributes dictionary for OpenTelemetry by formatting each value."""
    return {key: gentrace_format_otel_value(value) for key, value in attributes.items()}


def is_pydantic_v1() -> bool:
    """Checks if the installed Pydantic version is V1."""
    try:
        from pydantic import VERSION

        return VERSION.startswith("1.")
    except ImportError:
        return False


__all__ = [
    "gentrace_format_otel_attributes",
    "gentrace_format_otel_value",
    "_gentrace_json_dumps",
    "is_pydantic_v1",
    "check_otel_config_and_warn",
]
