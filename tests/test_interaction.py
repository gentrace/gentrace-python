import uuid
import asyncio
import unittest
from typing import Any, Dict, Tuple, Callable
from unittest.mock import MagicMock, patch

from opentelemetry.trace.status import Status, StatusCode

from gentrace.lib.utils import _gentrace_json_dumps
from gentrace.lib.constants import GENTRACE_FN_ARGS_EVENT_NAME, GENTRACE_FN_OUTPUT_EVENT_NAME
from gentrace.lib.interaction import interaction


class TestInteraction(unittest.TestCase):
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
    def test_interaction_sync_success(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer
        pipeline_id = str(uuid.uuid4())

        @interaction(pipeline_id=pipeline_id)
        def sync_process(data: Dict[str, Any]) -> Dict[str, Any]:
            return {**data, "processed": True}

        input_data = {"a": 1}
        result = sync_process(input_data)

        self.assertEqual(result, {"a": 1, "processed": True})
        mock_get_tracer.assert_called_once_with("gentrace")
        mock_tracer.start_as_current_span.assert_called_once_with("sync_process")

        mock_span.set_attributes.assert_called_once_with({"gentrace.pipeline_id": pipeline_id})

        expected_serialized_args = _gentrace_json_dumps([{"data": input_data}])
        mock_span.add_event.assert_any_call(GENTRACE_FN_ARGS_EVENT_NAME, {"args": expected_serialized_args})
        mock_span.add_event.assert_any_call(GENTRACE_FN_OUTPUT_EVENT_NAME, {"output": _gentrace_json_dumps(result)})
        mock_span.record_exception.assert_not_called()
        mock_span.set_status.assert_not_called()

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_interaction_sync_error(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer
        pipeline_id = str(uuid.uuid4())
        error = ValueError("Sync Interaction Error")

        @interaction(pipeline_id=pipeline_id)
        def sync_error_interaction() -> None:
            raise error

        with self.assertRaises(ValueError) as context:
            sync_error_interaction()

        self.assertTrue("Sync Interaction Error" in str(context.exception))
        mock_tracer.start_as_current_span.assert_called_once_with("sync_error_interaction")
        mock_span.set_attributes.assert_called_once_with({"gentrace.pipeline_id": pipeline_id})
        mock_span.record_exception.assert_called_once_with(error)

        mock_span.set_status.assert_called_once()
        called_status = mock_span.set_status.call_args[0][0]
        self.assertIsInstance(called_status, Status)
        self.assertEqual(called_status.status_code, StatusCode.ERROR)
        self.assertEqual(called_status.description, str(error))

        mock_span.set_attribute.assert_called_once_with("error.type", "ValueError")

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_interaction_custom_attributes_merged(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer
        pipeline_id = str(uuid.uuid4())
        user_attrs = {"user_key": "user_value", "other_key": 123}

        @interaction(pipeline_id=pipeline_id, attributes=user_attrs)
        def func_with_custom_attrs() -> str:
            return "done"

        func_with_custom_attrs()

        expected_attributes = {
            **user_attrs,
            "gentrace.pipeline_id": pipeline_id,
        }
        mock_span.set_attributes.assert_called_once_with(expected_attributes)

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_interaction_pipeline_id_precedence(self, mock_get_tracer: MagicMock) -> None:
        mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer
        pipeline_id = str(uuid.uuid4())
        user_attrs_with_conflict = {"gentrace.pipeline_id": "user-pipeline-id", "user_key": "value"}

        @interaction(pipeline_id=pipeline_id, attributes=user_attrs_with_conflict)
        def func_with_conflict() -> str:
            return "done"

        func_with_conflict()

        expected_attributes = {
            "user_key": "value",
            "gentrace.pipeline_id": pipeline_id,
        }
        mock_span.set_attributes.assert_called_once_with(expected_attributes)

    @patch("gentrace.lib.traced.trace.get_tracer")
    def test_interaction_anonymous_function_name(self, mock_get_tracer: MagicMock) -> None:
        _mock_span, mock_tracer = self.common_test_setup()
        mock_get_tracer.return_value = mock_tracer
        pipeline_id = str(uuid.uuid4())

        anon_interaction_func: Callable[[], str] = interaction(pipeline_id=pipeline_id)(lambda: "anon_result")
        anon_interaction_func()

        mock_tracer.start_as_current_span.assert_called_once_with("<lambda>")

    def test_interaction_sync_invalid_pipeline_id(self) -> None:
        invalid_id = "not-a-valid-uuid"
        with self.assertRaisesRegex(
            ValueError, f"Attribute 'gentrace.pipeline_id' must be a valid UUID string. Received: '{invalid_id}'"
        ):

            @interaction(pipeline_id=invalid_id)
            def sync_invalid_id_func() -> None:  # type: ignore
                pass

    def test_interaction_async_invalid_pipeline_id(self) -> None:
        invalid_id = "another-invalid-uuid"
        with self.assertRaisesRegex(
            ValueError, f"Attribute 'gentrace.pipeline_id' must be a valid UUID string. Received: '{invalid_id}'"
        ):

            @interaction(pipeline_id=invalid_id)
            async def async_invalid_id_func() -> None:  # type: ignore
                await asyncio.sleep(0)
                pass


if __name__ == "__main__":
    unittest.main()
