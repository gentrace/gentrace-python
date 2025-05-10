import uuid
import unittest
from typing import Tuple
from unittest.mock import MagicMock, patch

from opentelemetry.trace.status import Status, StatusCode

from gentrace.lib.traced import traced


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
        
        mock_span.add_event.assert_any_call(
            "gentrace.fn.args", {"args": "[2, 3]", "kwargs": "{}"}
        )
        mock_span.add_event.assert_any_call(
            "gentrace.fn.output", {"output": "5"}
        )
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
        mock_span.add_event.assert_any_call(
            "gentrace.fn.args", {"args": "[]", "kwargs": "{}"}
        )
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

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_traced_with_valid_pipeline_id_attribute(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer
        
        pipeline_id_uuid = str(uuid.uuid4())
        test_attributes = {"gentrace.pipeline_id": pipeline_id_uuid, "other_key": "value"}
        
        @traced(attributes=test_attributes)
        def func_with_pipeline_id_attr() -> str:
            return "done"

        func_with_pipeline_id_attr()
        
        mock_span.set_attributes.assert_called_once_with(test_attributes)

    def test_traced_with_invalid_pipeline_id_attribute_format(self) -> None:
        invalid_pipeline_id = "not-a-uuid"
        test_attributes = {"gentrace.pipeline_id": invalid_pipeline_id}
        
        with self.assertRaisesRegex(
            ValueError,
            f"Attribute 'gentrace.pipeline_id' must be a valid UUID string. Received: '{invalid_pipeline_id}'"
        ):
            @traced(attributes=test_attributes)
            def func_with_invalid_pipeline_id_attr() -> None: # type: ignore
                pass

    def test_traced_with_invalid_pipeline_id_attribute_type(self) -> None:
        invalid_pipeline_id_type = 12345
        test_attributes = {"gentrace.pipeline_id": invalid_pipeline_id_type}
        
        expected_error_msg = (
            f"Attribute 'gentrace.pipeline_id' must be a string representation of a UUID. "
            f"Received type: {type(invalid_pipeline_id_type)}, value: '{invalid_pipeline_id_type}'"
        )
        with self.assertRaisesRegex(
            ValueError,
            expected_error_msg
        ):
            @traced(attributes=test_attributes)
            def func_with_invalid_pipeline_id_type_attr() -> None: # type: ignore
                pass


if __name__ == "__main__":
    unittest.main() 