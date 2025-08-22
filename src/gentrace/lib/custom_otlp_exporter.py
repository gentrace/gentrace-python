"""
Custom OTLP Span Exporter for Gentrace

This exporter wraps our vendored OTLP exporter to add Gentrace-specific
functionality like partial success handling and custom error messages.
By using composition instead of inheritance, we avoid brittleness across
OpenTelemetry versions.
"""

import json
import logging
from typing import TYPE_CHECKING, Any, Sequence
from typing_extensions import override

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceResponse,
)

from .utils import display_gentrace_warning
from .warnings import GentraceWarnings
from .vendored_otlp_exporter import GentraceVendoredOTLPSpanExporter

if TYPE_CHECKING:
    import requests

_logger = logging.getLogger(__name__)


class GentraceOTLPSpanExporter(SpanExporter):
    """
    Custom OTLP Span Exporter that wraps the vendored exporter.
    
    This exporter uses composition to wrap our vendored OTLP exporter,
    adding Gentrace-specific functionality while maintaining stability
    across OpenTelemetry versions.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the custom exporter by creating a vendored exporter."""
        # Create the vendored exporter with the same arguments
        self._exporter = GentraceVendoredOTLPSpanExporter(*args, **kwargs)
        
        # Store original send_request method so we can intercept responses
        self._original_send_request = self._exporter._send_request
        self._exporter._send_request = self._intercepted_send_request  # type: ignore[method-assign]
        
        # Store original handle_error method so we can customize error messages
        self._original_handle_error = self._exporter._handle_error
        self._exporter._handle_error = self._handle_error_with_gentrace_warnings  # type: ignore[method-assign]

    @override
    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        """
        Export spans using the vendored exporter with our customizations.
        """
        return self._exporter.export(spans)

    @override
    def shutdown(self) -> None:
        """Shutdown the underlying exporter."""
        self._exporter.shutdown()

    @override
    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Force flush the underlying exporter."""
        return self._exporter.force_flush(timeout_millis)

    def _intercepted_send_request(self, data: bytes, timeout: float) -> "requests.Response":
        """
        Intercept the send_request to check for partial success on 200 OK responses.
        """
        # Call the original send_request
        resp = self._original_send_request(data, timeout)
        
        # If successful, check for partial success
        if resp.ok and resp.content:
            self._check_partial_success(resp)
        
        return resp

    def _handle_error_with_gentrace_warnings(self, resp: "requests.Response") -> None:
        """
        Handle errors with Gentrace-specific warnings.
        """
        if resp.status_code == 401:
            # Display the authentication error warning (only once per session)
            warning = GentraceWarnings.OtelAuthenticationError()
            display_gentrace_warning(warning)
        elif resp.status_code == 403:
            _logger.error(
                "Failed to export traces: Access forbidden (403). "
                "Your API key may not have the required permissions."
            )
        elif resp.status_code == 404:
            _logger.error(
                "Failed to export traces: Endpoint not found (404). "
                "Please check your Gentrace configuration."
            )
        else:
            # Fall back to the original error handler for other errors
            self._original_handle_error(resp)

    def _check_partial_success(self, resp: "requests.Response") -> None:
        """
        Check response for partial success indicators and display warnings.
        """
        try:
            # Check response content type
            content_type = resp.headers.get('content-type', '').lower()
            
            response_proto = None
            
            if 'application/json' in content_type:
                # Handle JSON response
                json_data = json.loads(resp.content.decode('utf-8'))
                
                # Check if this is a byte array encoded as JSON object with numeric keys
                if all(isinstance(k, str) and k.isdigit() for k in json_data.keys()):
                    # Convert JSON object with numeric keys to bytes
                    byte_array = bytes([json_data[str(i)] for i in range(len(json_data))])
                    
                    # Try to parse as protobuf
                    response_proto = ExportTraceServiceResponse()
                    response_proto.ParseFromString(byte_array)
                else:
                    # Normal JSON response
                    # Convert JSON to protobuf message
                    response_proto = ExportTraceServiceResponse()
                    if 'partialSuccess' in json_data:
                        partial_success_json = json_data['partialSuccess']
                        if 'rejectedSpans' in partial_success_json:
                            response_proto.partial_success.rejected_spans = int(
                                partial_success_json['rejectedSpans']
                            )
                        if 'errorMessage' in partial_success_json:
                            response_proto.partial_success.error_message = (
                                partial_success_json['errorMessage']
                            )
            else:
                # Handle protobuf response
                response_proto = ExportTraceServiceResponse()
                response_proto.ParseFromString(resp.content)

            # Check if partial_success field is present
            if response_proto and response_proto.HasField("partial_success"):
                partial_success = response_proto.partial_success

                # Check for rejected spans
                if partial_success.rejected_spans > 0 or partial_success.error_message:
                    # Display the warning using the Gentrace warning system
                    warning = GentraceWarnings.OtelPartialFailureWarning(
                        partial_success.rejected_spans,
                        partial_success.error_message
                    )
                    display_gentrace_warning(warning)
        except Exception as e:
            # Don't fail the export if we can't parse the response
            # This ensures backward compatibility
            _logger.debug(
                "Failed to parse OTLP response for partial success: %s",
                str(e),
            )