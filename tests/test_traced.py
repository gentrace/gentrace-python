import unittest
from typing import Tuple
from unittest.mock import MagicMock, patch

from opentelemetry.trace.status import Status, StatusCode

from gentrace.lib.traced import traced
from gentrace.lib.constants import ATTR_GENTRACE_FN_ARGS_EVENT_NAME, ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME


class TestTraced(unittest.TestCase):
    def common_test_setup(self) -> Tuple[MagicMock, MagicMock]:
        mock_span = MagicMock()
        mock_span.set_attribute = MagicMock()
        mock_span.set_attributes = MagicMock()
        mock_span.add_event = MagicMock()
        mock_span.record_exception = MagicMock()
        mock_span.set_status = MagicMock()
        mock_span.end = MagicMock()

        mock_tracer = MagicMock()
        mock_tracer.start_as_current_span.return_value.__enter__.return_value = mock_span

        return mock_span, mock_tracer

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_traced_sync_function_success(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer

        @traced()
        def sync_add(a: int, b: int) -> int:
            return a + b

        result = sync_add(2, 3)

        self.assertEqual(result, 5)
        mock_get_tracer.assert_called_once_with("gentrace")
        mock_tracer.start_as_current_span.assert_called_once_with("sync_add")

        mock_span.add_event.assert_any_call(ATTR_GENTRACE_FN_ARGS_EVENT_NAME, {"args": '[{"a": 2}, {"b": 3}]'})
        mock_span.add_event.assert_any_call(ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME, {"output": "5"})
        mock_span.record_exception.assert_not_called()
        mock_span.set_status.assert_not_called()

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_traced_sync_function_error(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer

        error = ValueError("Sync Error")

        @traced()
        def sync_error_func() -> None:
            raise error

        with self.assertRaises(ValueError) as context:
            sync_error_func()

        self.assertTrue("Sync Error" in str(context.exception))
        mock_get_tracer.assert_called_once_with("gentrace")
        mock_tracer.start_as_current_span.assert_called_once_with("sync_error_func")
        mock_span.add_event.assert_any_call(ATTR_GENTRACE_FN_ARGS_EVENT_NAME, {"args": "[]"})
        mock_span.record_exception.assert_called_once_with(error)

        mock_span.set_status.assert_called_once()
        called_status = mock_span.set_status.call_args[0][0]
        self.assertIsInstance(called_status, Status)
        self.assertEqual(called_status.status_code, StatusCode.ERROR)
        self.assertEqual(called_status.description, "Sync Error")

        mock_span.set_attribute.assert_called_once_with("error.type", "ValueError")

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_traced_custom_name(self, mock_get_tracer: MagicMock) -> None:
        _mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer

        @traced(name="custom_span_name")
        def original_name_func() -> str:
            return "result"

        original_name_func()
        mock_tracer.start_as_current_span.assert_called_once_with("custom_span_name")

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_traced_anonymous_function_name(self, mock_get_tracer: MagicMock) -> None:
        _mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer

        anon_func = traced()(lambda: "anon_result")
        anon_func()

        mock_tracer.start_as_current_span.assert_called_once_with("<lambda>")

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_traced_attributes_passed(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer

        test_attributes = {"key1": "value1", "key2": 123}

        with patch("gentrace.lib.traced.gentrace_format_otel_attributes") as mock_format_attributes:
            formatted_attributes = {"gentrace.key1": "value1", "gentrace.key2": 123}
            mock_format_attributes.return_value = formatted_attributes

            @traced(attributes=test_attributes)
            def func_with_attrs() -> str:
                return "done"

            func_with_attrs()

            mock_format_attributes.assert_called_once_with(test_attributes)
            mock_span.set_attributes.assert_called_once_with(formatted_attributes)

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_traced_no_attributes(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer

        @traced()
        def func_no_attrs() -> str:
            return "done"

        func_no_attrs()
        mock_span.set_attributes.assert_not_called()


if __name__ == "__main__":
    unittest.main()
