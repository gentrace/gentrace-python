"""Type definitions for the Gentrace library."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional
from typing_extensions import TypedDict

if TYPE_CHECKING:
    from opentelemetry.sdk.trace.sampling import Sampler  # type: ignore

    _ = Sampler  # Keep import for type checking
else:
    Sampler = Any


class OtelConfigOptions(TypedDict, total=False):
    """
    Configuration options for OpenTelemetry setup.

    All fields are optional. When not provided, sensible defaults are used.
    """

    trace_endpoint: Optional[str]
    """Custom OTLP endpoint URL. Defaults to Gentrace's OTLP endpoint."""

    service_name: Optional[str]
    """Service name for the application. Auto-detected from pyproject.toml if not provided."""

    instrumentations: Optional[List[Any]]
    """List of OpenTelemetry instrumentation instances to configure."""

    resource_attributes: Optional[Dict[str, Any]]
    """Additional resource attributes to include in all spans."""

    sampler: Optional[Any]  # Actually Optional[Sampler] but using Any for compatibility
    """Custom sampler for trace sampling. Defaults to standard OpenTelemetry behavior."""

    debug: bool
    """Enable console exporter for debugging. Defaults to False."""


__all__ = ["OtelConfigOptions"]
