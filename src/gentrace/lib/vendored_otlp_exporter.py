"""
Vendored OTLP Span Exporter for Gentrace

This is a simplified, stable implementation of an OTLP span exporter that doesn't
depend on OpenTelemetry's internal APIs. It directly implements the OTLP protocol
for exporting spans, avoiding brittleness from subclassing across versions.

Why we vendored this exporter:
---------------------------------
Between OpenTelemetry SDK versions 1.32 and 1.36, there were significant internal
API changes in the OTLPSpanExporter class:

1. Version 1.32 and earlier:
   - Used a method called `_export_serialized_spans` for the export logic
   - Had a function called `_serialize_spans` to convert spans to protobuf
   - Used `_retryable` function to check if errors should be retried

2. Version 1.36 and later:
   - Removed `_export_serialized_spans` entirely
   - Replaced `_serialize_spans` with `encode_spans` from a different module
   - Renamed `_retryable` to `_is_retryable` and moved it to a different location

These breaking changes in internal APIs meant that our custom exporter, which
previously subclassed OTLPSpanExporter, would break whenever users upgraded their
OpenTelemetry SDK version. Since we need to support a wide range of OpenTelemetry
versions (1.21.0+), we decided to vendor the exporter implementation.

This vendored implementation:
- Only uses stable, public OpenTelemetry APIs (SpanExporter, ReadableSpan, protobuf messages)
- Implements the OTLP protocol directly without depending on internal implementation details
- Will remain stable across OpenTelemetry version upgrades
- Provides the same functionality as the original OTLPSpanExporter but with better stability

Based on OpenTelemetry Python SDK but simplified for stability and maintainability.
"""

import gzip
import json
import zlib
import random
import logging
import threading
from io import BytesIO
from os import environ
from enum import Enum
from time import time
from typing import Any, Dict, List, Optional, Sequence
from collections import defaultdict
from typing_extensions import override

import requests
from opentelemetry.trace import Status, SpanKind, StatusCode
from opentelemetry.util.re import parse_env_headers
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.proto.trace.v1.trace_pb2 import (
    Span as PB2Span,
    Status as PB2Status,
    ScopeSpans,
    ResourceSpans,
)

# These imports are stable public APIs
from opentelemetry.sdk.environment_variables import (
    OTEL_EXPORTER_OTLP_HEADERS,
    OTEL_EXPORTER_OTLP_TIMEOUT,
    OTEL_EXPORTER_OTLP_ENDPOINT,
    OTEL_EXPORTER_OTLP_COMPRESSION,
    OTEL_EXPORTER_OTLP_TRACES_HEADERS,
    OTEL_EXPORTER_OTLP_TRACES_TIMEOUT,
    OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
    OTEL_EXPORTER_OTLP_TRACES_COMPRESSION,
)
from opentelemetry.proto.common.v1.common_pb2 import (
    AnyValue,
    KeyValue,
    ArrayValue,
    InstrumentationScope,
)
from opentelemetry.proto.resource.v1.resource_pb2 import Resource as PB2Resource

# Import protobuf messages - these are stable
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTraceServiceRequest,
    ExportTraceServiceResponse,
)

from .utils import display_gentrace_warning
from .warnings import GentraceWarnings

_logger = logging.getLogger(__name__)

# Constants
DEFAULT_ENDPOINT = "http://localhost:4318/"
DEFAULT_TRACES_EXPORT_PATH = "v1/traces"
DEFAULT_TIMEOUT = 10  # in seconds
MAX_RETRIES = 6

# Headers for OTLP/HTTP
OTLP_HTTP_HEADERS = {
    "Content-Type": "application/x-protobuf",
}


class Compression(Enum):
    """Compression algorithms for OTLP export."""
    NoCompression = "none"
    Gzip = "gzip"
    Deflate = "deflate"


class GentraceVendoredOTLPSpanExporter(SpanExporter):
    """
    A vendored OTLP Span Exporter that doesn't depend on OpenTelemetry internals.
    
    This exporter directly implements the OTLP protocol for exporting spans,
    providing stability across different OpenTelemetry versions.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        compression: Optional[Compression] = None,
        session: Optional[requests.Session] = None,
    ):
        """Initialize the vendored OTLP exporter."""
        self._shutdown_in_progress = threading.Event()
        self._shutdown = False
        
        # Configure endpoint
        self._endpoint = endpoint or environ.get(
            OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
            self._append_trace_path(
                environ.get(OTEL_EXPORTER_OTLP_ENDPOINT, DEFAULT_ENDPOINT)
            ),
        )
        
        # Configure headers
        headers_string = environ.get(
            OTEL_EXPORTER_OTLP_TRACES_HEADERS,
            environ.get(OTEL_EXPORTER_OTLP_HEADERS, ""),
        )
        self._headers = headers or parse_env_headers(headers_string, liberal=True)
        
        # Configure timeout
        self._timeout = timeout or float(
            environ.get(
                OTEL_EXPORTER_OTLP_TRACES_TIMEOUT,
                environ.get(OTEL_EXPORTER_OTLP_TIMEOUT, DEFAULT_TIMEOUT),
            )
        )
        
        # Configure compression
        self._compression = compression or self._compression_from_env()
        
        # Setup session
        self._session = session or requests.Session()
        self._session.headers.update(self._headers)
        self._session.headers.update(OTLP_HTTP_HEADERS)
        
        if self._compression != Compression.NoCompression:
            self._session.headers.update(
                {"Content-Encoding": self._compression.value}
            )

    @override
    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        """Export spans to the OTLP endpoint."""
        if self._shutdown:
            _logger.warning("Exporter already shutdown, ignoring batch")
            return SpanExportResult.FAILURE

        # Encode spans to protobuf
        serialized_data = self._encode_spans(spans).SerializePartialToString()
        
        # Apply compression if needed
        data = self._compress_data(serialized_data)
        
        deadline_sec = time() + self._timeout
        
        for retry_num in range(MAX_RETRIES):
            try:
                resp = self._send_request(data, deadline_sec - time())
                
                if resp.ok:
                    # Check for partial success
                    if resp.content:
                        self._check_partial_success(resp)
                    return SpanExportResult.SUCCESS
                
                # Handle retries
                if not self._is_retryable(resp):
                    self._handle_error(resp)
                    return SpanExportResult.FAILURE
                
                if retry_num + 1 == MAX_RETRIES:
                    _logger.error(
                        "Max retries reached. Failed to export spans: %s",
                        resp.text,
                    )
                    return SpanExportResult.FAILURE
                
                # Calculate backoff with jitter
                backoff_seconds = 2**retry_num * random.uniform(0.8, 1.2)
                
                if backoff_seconds > (deadline_sec - time()):
                    _logger.error("Export deadline exceeded, aborting retries")
                    return SpanExportResult.FAILURE
                
                _logger.warning(
                    "Transient error %s encountered, retrying in %.2fs",
                    resp.reason,
                    backoff_seconds,
                )
                
                if self._shutdown_in_progress.wait(backoff_seconds):
                    _logger.warning("Shutdown in progress, aborting retry")
                    return SpanExportResult.FAILURE
                    
            except Exception as e:
                _logger.error("Failed to export spans: %s", str(e))
                return SpanExportResult.FAILURE
        
        return SpanExportResult.FAILURE

    @override
    def shutdown(self) -> None:
        """Shutdown the exporter."""
        if self._shutdown:
            _logger.warning("Exporter already shutdown, ignoring call")
            return
        self._shutdown = True
        self._shutdown_in_progress.set()
        self._session.close()

    @override
    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Nothing is buffered in this exporter."""
        _ = timeout_millis  # Unused but part of the interface
        return True

    # Private helper methods

    def _append_trace_path(self, endpoint: str) -> str:
        """Append the traces path to the endpoint."""
        if endpoint.endswith("/"):
            return endpoint + DEFAULT_TRACES_EXPORT_PATH
        return endpoint + f"/{DEFAULT_TRACES_EXPORT_PATH}"

    def _compression_from_env(self) -> Compression:
        """Get compression setting from environment."""
        compression = (
            environ.get(
                OTEL_EXPORTER_OTLP_TRACES_COMPRESSION,
                environ.get(OTEL_EXPORTER_OTLP_COMPRESSION, "none"),
            )
            .lower()
            .strip()
        )
        try:
            return Compression(compression)
        except ValueError:
            _logger.warning("Unknown compression type %s, using none", compression)
            return Compression.NoCompression

    def _compress_data(self, data: bytes) -> bytes:
        """Compress data based on compression setting."""
        if self._compression == Compression.Gzip:
            gzip_data = BytesIO()
            with gzip.GzipFile(fileobj=gzip_data, mode="w") as gzip_stream:
                gzip_stream.write(data)
            return gzip_data.getvalue()
        elif self._compression == Compression.Deflate:
            return zlib.compress(data)
        return data

    def _send_request(self, data: bytes, timeout: float) -> requests.Response:
        """Send the export request with retry on connection errors."""
        try:
            return self._session.post(
                url=self._endpoint,  # type: ignore[arg-type]
                data=data,
                timeout=timeout,
            )
        except requests.exceptions.ConnectionError:
            # Retry once on connection error
            return self._session.post(
                url=self._endpoint,  # type: ignore[arg-type]
                data=data,
                timeout=timeout,
            )

    def _is_retryable(self, resp: requests.Response) -> bool:
        """Check if the response indicates a retryable error."""
        if resp.status_code == 408:  # Request Timeout
            return True
        if 500 <= resp.status_code <= 599:  # Server errors
            return True
        return False

    def _handle_error(self, resp: requests.Response) -> None:
        """Handle non-retryable errors with appropriate logging."""
        if resp.status_code == 401:
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
            _logger.error(
                "Failed to export traces: HTTP %s error, reason: %s",
                resp.status_code,
                resp.text,
            )

    def _check_partial_success(self, resp: requests.Response) -> None:
        """Check response for partial success indicators."""
        try:
            content_type = resp.headers.get('content-type', '').lower()
            response_proto = None
            
            if 'application/json' in content_type:
                # Handle JSON response
                json_data = json.loads(resp.content.decode('utf-8'))
                
                # Check if this is a byte array encoded as JSON
                if all(isinstance(k, str) and k.isdigit() for k in json_data.keys()):
                    byte_array = bytes([json_data[str(i)] for i in range(len(json_data))])
                    response_proto = ExportTraceServiceResponse()
                    response_proto.ParseFromString(byte_array)
                else:
                    # Parse JSON partial success
                    response_proto = ExportTraceServiceResponse()
                    if 'partialSuccess' in json_data:
                        partial = json_data['partialSuccess']
                        if 'rejectedSpans' in partial:
                            response_proto.partial_success.rejected_spans = int(partial['rejectedSpans'])
                        if 'errorMessage' in partial:
                            response_proto.partial_success.error_message = partial['errorMessage']
            else:
                # Handle protobuf response
                response_proto = ExportTraceServiceResponse()
                response_proto.ParseFromString(resp.content)

            # Check for partial success
            if response_proto and response_proto.HasField("partial_success"):
                partial = response_proto.partial_success
                if partial.rejected_spans > 0 or partial.error_message:
                    warning = GentraceWarnings.OtelPartialFailureWarning(
                        partial.rejected_spans,
                        partial.error_message
                    )
                    display_gentrace_warning(warning)
                    
        except Exception as e:
            _logger.debug("Failed to parse OTLP response: %s", str(e))

    def _encode_spans(self, spans: Sequence[ReadableSpan]) -> ExportTraceServiceRequest:
        """Encode spans to OTLP protobuf format."""
        # Group spans by resource and instrumentation scope
        resource_spans_map = defaultdict(lambda: defaultdict(list))  # type: ignore[var-annotated]
        
        for span in spans:
            resource = span.resource
            scope = span.instrumentation_scope or None
            pb_span = self._encode_span(span)
            resource_spans_map[resource][scope].append(pb_span)  # type: ignore[index]
        
        # Build the protobuf message
        resource_spans_list = []
        for resource, scope_map in resource_spans_map.items():  # type: ignore[assignment]
            scope_spans_list = []
            for scope, pb_spans in scope_map.items():  # type: ignore[assignment]
                scope_spans = ScopeSpans(
                    scope=self._encode_instrumentation_scope(scope) if scope else None,
                    spans=pb_spans,  # type: ignore[arg-type]
                    schema_url=scope.schema_url if scope else None,  # type: ignore[arg-type, union-attr]
                )
                scope_spans_list.append(scope_spans)  # type: ignore[arg-type]
            
            resource_spans = ResourceSpans(
                resource=self._encode_resource(resource),
                scope_spans=scope_spans_list,  # type: ignore[arg-type]
                schema_url=resource.schema_url if hasattr(resource, 'schema_url') else None,  # type: ignore[arg-type, union-attr]
            )
            resource_spans_list.append(resource_spans)  # type: ignore[arg-type]
        
        return ExportTraceServiceRequest(resource_spans=resource_spans_list)  # type: ignore[arg-type]

    def _encode_span(self, span: ReadableSpan) -> PB2Span:
        """Encode a single span to protobuf format."""
        # Map span kind
        span_kind_map = {
            SpanKind.INTERNAL: PB2Span.SpanKind.SPAN_KIND_INTERNAL,
            SpanKind.SERVER: PB2Span.SpanKind.SPAN_KIND_SERVER,
            SpanKind.CLIENT: PB2Span.SpanKind.SPAN_KIND_CLIENT,
            SpanKind.PRODUCER: PB2Span.SpanKind.SPAN_KIND_PRODUCER,
            SpanKind.CONSUMER: PB2Span.SpanKind.SPAN_KIND_CONSUMER,
        }
        
        pb_span = PB2Span(
            trace_id=span.context.trace_id.to_bytes(16, "big"),  # type: ignore[union-attr]
            span_id=span.context.span_id.to_bytes(8, "big"),  # type: ignore[union-attr]
            name=span.name,
            kind=span_kind_map.get(span.kind, PB2Span.SpanKind.SPAN_KIND_UNSPECIFIED),
            start_time_unix_nano=span.start_time,  # type: ignore[arg-type]
            end_time_unix_nano=span.end_time,  # type: ignore[arg-type]
            attributes=self._encode_attributes(span.attributes),  # type: ignore[arg-type]
        )
        
        # Set parent span ID if present
        if span.parent and span.parent.span_id:
            pb_span.parent_span_id = span.parent.span_id.to_bytes(8, "big")
        
        # Set status if present
        if span.status:
            pb_span.status.CopyFrom(self._encode_status(span.status))
        
        # Add events
        if span.events:
            for event in span.events:
                pb_event = PB2Span.Event(
                    time_unix_nano=event.timestamp,
                    name=event.name,
                    attributes=self._encode_attributes(event.attributes),  # type: ignore[arg-type]
                )
                pb_span.events.append(pb_event)
        
        # Add links
        if span.links:
            for link in span.links:
                pb_link = PB2Span.Link(
                    trace_id=link.context.trace_id.to_bytes(16, "big"),
                    span_id=link.context.span_id.to_bytes(8, "big"),
                    attributes=self._encode_attributes(link.attributes),  # type: ignore[arg-type]
                )
                pb_span.links.append(pb_link)
        
        return pb_span

    def _encode_status(self, status: Status) -> PB2Status:
        """Encode span status to protobuf format."""
        
        status_code_map = {
            StatusCode.UNSET: PB2Status.StatusCode.STATUS_CODE_UNSET,
            StatusCode.OK: PB2Status.StatusCode.STATUS_CODE_OK,
            StatusCode.ERROR: PB2Status.StatusCode.STATUS_CODE_ERROR,
        }
        
        pb_status = PB2Status(
            code=status_code_map.get(status.status_code, PB2Status.StatusCode.STATUS_CODE_UNSET)
        )
        if status.description:
            pb_status.message = status.description
        return pb_status

    def _encode_resource(self, resource: Any) -> PB2Resource:
        """Encode resource to protobuf format."""
        if not resource:
            return PB2Resource()
        return PB2Resource(
            attributes=self._encode_attributes(resource.attributes)
        )

    def _encode_instrumentation_scope(self, scope: Any) -> InstrumentationScope:
        """Encode instrumentation scope to protobuf format."""
        if not scope:
            return InstrumentationScope()
        
        pb_scope = InstrumentationScope(name=scope.name)
        if scope.version:
            pb_scope.version = scope.version
        if hasattr(scope, 'attributes') and scope.attributes:
            pb_scope.attributes.extend(self._encode_attributes(scope.attributes))
        return pb_scope

    def _encode_attributes(self, attributes: Optional[Dict[str, Any]]) -> List[KeyValue]:
        """Encode attributes to protobuf format."""
        if not attributes:
            return []
        
        pb_attributes = []
        for key, value in attributes.items():
            pb_attributes.append(KeyValue(  # type: ignore[attr-defined]
                key=key,
                value=self._encode_value(value)
            ))  # type: ignore[arg-type]
        return pb_attributes  # type: ignore[return-value]

    def _encode_value(self, value: Any) -> AnyValue:
        """Encode a single value to protobuf format."""
        any_value = AnyValue()
        
        if value is None:
            pass  # Leave as default (unset)
        elif isinstance(value, bool):
            any_value.bool_value = value
        elif isinstance(value, int):
            any_value.int_value = value
        elif isinstance(value, float):
            any_value.double_value = value
        elif isinstance(value, str):
            any_value.string_value = value
        elif isinstance(value, bytes):
            any_value.bytes_value = value
        elif isinstance(value, (list, tuple)):
            array_value = ArrayValue()
            for item in value:  # type: ignore[misc]
                array_value.values.append(self._encode_value(item))
            any_value.array_value.CopyFrom(array_value)
        else:
            # Fallback to string representation
            any_value.string_value = str(value)
        
        return any_value