import logging
from typing import List
from unittest.mock import Mock, patch

import pytest
from pytest import LogCaptureFixture
from opentelemetry.sdk.trace.export import SpanExportResult
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import (
    ExportTracePartialSuccess,
    ExportTraceServiceResponse,
)

from gentrace.lib.custom_otlp_exporter import GentraceOTLPSpanExporter


@pytest.fixture
def mock_spans() -> List[Mock]:
    """Create mock spans for testing."""
    span = Mock()
    span.name = "test_span"
    return [span]


@pytest.fixture
def exporter() -> GentraceOTLPSpanExporter:
    """Create an exporter instance for testing."""
    return GentraceOTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces",
        headers={"Authorization": "Bearer test-key"},
    )


class TestCustomOTLPExporter:
    """Test cases for the custom OTLP exporter with partial success handling."""

    def test_successful_export_without_partial_success(
        self, exporter: GentraceOTLPSpanExporter, mock_spans: List[Mock], caplog: LogCaptureFixture
    ) -> None:
        """Test successful export without partial success response."""
        # Mock response without body
        mock_response = Mock()
        mock_response.ok = True
        mock_response.content = b""  # Empty content
        mock_response.headers = {"content-type": "application/x-protobuf"}

        with patch.object(exporter, "_serialize_spans", return_value=b"serialized"):
            with patch.object(exporter, "_export", return_value=mock_response):
                result = exporter.export(mock_spans)

        assert result == SpanExportResult.SUCCESS
        # No warnings should be logged
        assert "partial success" not in caplog.text.lower()

    def test_export_with_rejected_spans(
        self, exporter: GentraceOTLPSpanExporter, mock_spans: List[Mock]
    ) -> None:
        """Test export with partial success - some spans rejected."""
        # Create partial success response
        partial_success = ExportTracePartialSuccess()
        partial_success.rejected_spans = 5
        partial_success.error_message = "Some spans were invalid"

        response_proto = ExportTraceServiceResponse()
        response_proto.partial_success.CopyFrom(partial_success)

        # Mock response with partial success
        mock_response = Mock()
        mock_response.ok = True
        mock_response.content = response_proto.SerializeToString()
        mock_response.headers = {"content-type": "application/x-protobuf"}

        with patch.object(exporter, "_serialize_spans", return_value=b"serialized"):
            with patch.object(exporter, "_export", return_value=mock_response):
                with patch("gentrace.lib.custom_otlp_exporter.display_gentrace_warning") as mock_display_warning:
                    result = exporter.export(mock_spans)

        assert result == SpanExportResult.SUCCESS
        # Check that warning was displayed
        mock_display_warning.assert_called_once()
        warning = mock_display_warning.call_args[0][0]
        assert warning.warning_id == "GT_OtelPartialFailureWarning"
        assert "5" in warning.get_simple_message()
        assert "Some spans were invalid" in warning.get_simple_message()

    def test_export_with_warning_message_only(
        self, exporter: GentraceOTLPSpanExporter, mock_spans: List[Mock]
    ) -> None:
        """Test export with warning message but no rejected spans."""
        # Create partial success response with warning only
        partial_success = ExportTracePartialSuccess()
        partial_success.rejected_spans = 0
        partial_success.error_message = "Consider using batch export for better performance"

        response_proto = ExportTraceServiceResponse()
        response_proto.partial_success.CopyFrom(partial_success)

        # Mock response
        mock_response = Mock()
        mock_response.ok = True
        mock_response.content = response_proto.SerializeToString()
        mock_response.headers = {"content-type": "application/x-protobuf"}

        with patch.object(exporter, "_serialize_spans", return_value=b"serialized"):
            with patch.object(exporter, "_export", return_value=mock_response):
                with patch("gentrace.lib.custom_otlp_exporter.display_gentrace_warning") as mock_display_warning:
                    result = exporter.export(mock_spans)

        assert result == SpanExportResult.SUCCESS
        # Check that warning was displayed
        mock_display_warning.assert_called_once()
        warning = mock_display_warning.call_args[0][0]
        assert warning.warning_id == "GT_OtelPartialFailureWarning"
        assert "Consider using batch export for better performance" in warning.get_simple_message()

    def test_export_with_parse_error(
        self, exporter: GentraceOTLPSpanExporter, mock_spans: List[Mock], caplog: LogCaptureFixture
    ) -> None:
        """Test that parse errors don't break the export."""
        # Mock response with invalid protobuf data
        mock_response = Mock()
        mock_response.ok = True
        mock_response.content = b"invalid protobuf data"
        mock_response.headers = {"content-type": "application/x-protobuf"}

        with patch.object(exporter, "_serialize_spans", return_value=b"serialized"):
            with patch.object(exporter, "_export", return_value=mock_response):
                with caplog.at_level(logging.DEBUG):
                    result = exporter.export(mock_spans)

        assert result == SpanExportResult.SUCCESS
        # Check that debug message was logged but export still succeeded
        assert "Failed to parse OTLP response for partial success" in caplog.text

    def test_export_failure(
        self, exporter: GentraceOTLPSpanExporter, mock_spans: List[Mock], caplog: LogCaptureFixture
    ) -> None:
        """Test export failure scenario."""
        # Mock failed response
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_response.reason = "Bad Request"

        with patch.object(exporter, "_serialize_spans", return_value=b"serialized"):
            with patch.object(exporter, "_export", return_value=mock_response):
                with patch.object(exporter, "_retryable", return_value=False):
                    with caplog.at_level(logging.ERROR):
                        result = exporter.export(mock_spans)

        assert result == SpanExportResult.FAILURE
        assert "Failed to export traces: HTTP 400 error" in caplog.text

    def test_retry_behavior(
        self, exporter: GentraceOTLPSpanExporter, mock_spans: List[Mock], caplog: LogCaptureFixture
    ) -> None:
        """Test retry behavior for transient errors."""
        # Mock responses - first fails with retryable error, then succeeds
        mock_response_fail = Mock()
        mock_response_fail.ok = False
        mock_response_fail.status_code = 503
        mock_response_fail.reason = "Service Unavailable"

        mock_response_success = Mock()
        mock_response_success.ok = True
        mock_response_success.content = b""

        responses = [mock_response_fail, mock_response_success]

        with patch.object(exporter, "_serialize_spans", return_value=b"serialized"):
            with patch.object(exporter, "_export", side_effect=responses):
                with patch.object(exporter, "_retryable", side_effect=[True, False]):
                    with patch("time.sleep"):  # Mock sleep to speed up test
                        with caplog.at_level(logging.WARNING):
                            result = exporter.export(mock_spans)

        assert result == SpanExportResult.SUCCESS
        assert "Transient error Service Unavailable encountered" in caplog.text