import logging
from typing import TYPE_CHECKING, Dict, Union, Iterator, Optional
from itertools import count
from typing_extensions import Literal, override

from opentelemetry.sdk.trace.export import SpanExportResult
from opentelemetry.exporter.otlp.proto.http import Compression
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceResponse,
)

from .utils import display_gentrace_warning
from .warnings import GentraceWarnings

if TYPE_CHECKING:
    import requests

_logger = logging.getLogger(__name__)


def _create_exp_backoff_generator(max_value: int = 0) -> Iterator[int]:
    """
    Creates an exponential backoff generator matching OpenTelemetry's implementation.
    
    This is reimplemented here to avoid importing from private modules.
    """
    for i in count(0):
        out = 2**i
        yield min(out, max_value) if max_value else out


class GentraceOTLPSpanExporter(OTLPSpanExporter):
    """
    Custom OTLP Span Exporter that extends the default OTLPSpanExporter
    to handle partial success responses from the OTLP endpoint.

    This exporter parses the response body even for successful (200 OK) responses
    and logs warnings when spans are partially rejected or when the server
    sends warning messages.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        certificate_file: Optional[str] = None,
        client_key_file: Optional[str] = None,
        client_certificate_file: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        compression: Optional[Compression] = None,
        session: Optional["requests.Session"] = None,
    ):
        """Initialize the custom exporter with the same parameters as the base class."""
        super().__init__(
            endpoint=endpoint,
            certificate_file=certificate_file,
            client_key_file=client_key_file,
            client_certificate_file=client_certificate_file,
            headers=headers,
            timeout=timeout,
            compression=compression,
            session=session,
        )

    @override
    def _export_serialized_spans(
        self, serialized_data: bytes
    ) -> Union[Literal[SpanExportResult.FAILURE], Literal[SpanExportResult.SUCCESS]]:
        """
        Override to add partial success checking while keeping parent's retry logic.
        
        This is a minimal override that adds our custom logic only when needed.
        """
        # Use the parent's retry logic directly
        for delay in _create_exp_backoff_generator(
            max_value=self._MAX_RETRY_TIMEOUT
        ):
            if delay == self._MAX_RETRY_TIMEOUT:
                return SpanExportResult.FAILURE

            resp = self._export(serialized_data)
            
            if resp.ok:
                # Add our partial success check here
                if resp.content:
                    self._check_partial_success(resp)
                return SpanExportResult.SUCCESS
            elif self._retryable(resp):
                _logger.warning(
                    "Transient error %s encountered while exporting span batch, retrying in %ss.",
                    resp.reason,
                    delay,
                )
                from time import sleep
                sleep(delay)
                continue
            else:
                # Provide clear error messages based on status code
                if resp.status_code == 401:
                    # Display the authentication error warning (only once per session)
                    warning = GentraceWarnings.OtelAuthenticationError()
                    display_gentrace_warning(warning)
                elif resp.status_code == 403:
                    _logger.error(
                        "Failed to export traces: Access forbidden (403). Your API key may not have the required permissions."
                    )
                elif resp.status_code == 404:
                    _logger.error(
                        "Failed to export traces: Endpoint not found (404). Please check your Gentrace configuration."
                    )
                else:
                    _logger.error(
                        "Failed to export traces: HTTP %s error",
                        resp.status_code,
                    )
                return SpanExportResult.FAILURE
        
        return SpanExportResult.FAILURE

    def _check_partial_success(self, resp: "requests.Response") -> None:
        """
        Check response for partial success indicators and display warnings.
        
        This method is isolated from the main export logic to minimize
        differences from the parent class.
        """
        try:
            # Check response content type
            content_type = resp.headers.get('content-type', '').lower()
            
            response_proto = None
            
            if 'application/json' in content_type:
                # Handle JSON response
                import json
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
                            response_proto.partial_success.rejected_spans = int(partial_success_json['rejectedSpans'])
                        if 'errorMessage' in partial_success_json:
                            response_proto.partial_success.error_message = partial_success_json['errorMessage']
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