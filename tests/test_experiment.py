import sys
import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest import LogCaptureFixture

from gentrace.lib.experiment import (
    ExperimentOptions,
    experiment,
    register_eval_function,
    get_current_experiment_context,
)

# Get a direct reference to the module where experiment() is defined
experiment_module_object = sys.modules["gentrace.lib.experiment"]


@pytest.mark.asyncio
async def test_experiment_decorator_simple_async_function() -> None:
    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "test_experiment_id"

        @experiment(pipeline_id="test_pipeline")
        async def sample_async_function() -> str:
            return "result"

        result = await sample_async_function()

        assert result == "result"
        mock_start_api.assert_called_once_with(pipelineId="test_pipeline", name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="test_experiment_id")


@pytest.mark.asyncio
async def test_experiment_decorator_simple_sync_function() -> None:
    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "test_experiment_id_sync"

        @experiment(pipeline_id="test_pipeline_sync")
        def sample_sync_function() -> str:
            return "sync_result"

        # Even though sample_sync_function is sync, the decorator makes it awaitable
        result = await sample_sync_function()

        assert result == "sync_result"
        mock_start_api.assert_called_once_with(pipelineId="test_pipeline_sync", name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="test_experiment_id_sync")


@pytest.mark.asyncio
async def test_experiment_context_is_set_and_retrievable() -> None:
    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_context_test"

        @experiment(pipeline_id="pipeline_for_context")
        async def function_with_context_check() -> None:
            context = get_current_experiment_context()
            assert context is not None
            assert context["experiment_id"] == "exp_id_context_test"
            assert context["pipeline_id"] == "pipeline_for_context"

            # Check context variable directly too
            raw_context = experiment_module_object.experiment_context_var.get()
            assert raw_context is not None
            assert raw_context["experiment_id"] == "exp_id_context_test"
            assert raw_context["pipeline_id"] == "pipeline_for_context"

        await function_with_context_check()

        # Context should be reset outside the function
        assert experiment_module_object.experiment_context_var.get() is None
        assert get_current_experiment_context() is None

        mock_start_api.assert_called_once_with(pipelineId="pipeline_for_context", name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_context_test")


@pytest.mark.asyncio
async def test_get_current_experiment_context_outside_experiment() -> None:
    assert get_current_experiment_context() is None
    assert experiment_module_object.experiment_context_var.get() is None


@pytest.mark.asyncio
async def test_experiment_decorator_with_options() -> None:
    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_options_test"
        experiment_name = "My Test Experiment"
        experiment_metadata = {"version": "1.0", "user": "test_user"}

        options: ExperimentOptions = {
            "name": experiment_name,
            "metadata": experiment_metadata,
        }

        @experiment(pipeline_id="pipeline_with_options", options=options)
        async def function_with_options() -> str:
            return "options_result"

        result = await function_with_options()

        assert result == "options_result"
        mock_start_api.assert_called_once_with(
            pipelineId="pipeline_with_options",
            name=experiment_name,
            metadata=experiment_metadata,
        )
        mock_finish_api.assert_called_once_with(id="exp_id_options_test")


@pytest.mark.asyncio
async def test_experiment_decorator_start_api_fails() -> None:
    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.side_effect = ValueError("API start failed")

        @experiment(pipeline_id="pipeline_api_fail")
        async def function_where_api_fails() -> str:
            # This part should not be reached
            return "should_not_return"

        with pytest.raises(ValueError, match="API start failed"):
            await function_where_api_fails()

        mock_start_api.assert_called_once_with(pipelineId="pipeline_api_fail", name=None, metadata=None)
        mock_finish_api.assert_not_called()
        # Context should not be set if start_api failed before setting it
        assert experiment_module_object.experiment_context_var.get() is None


@pytest.mark.asyncio
async def test_experiment_with_sync_eval_function() -> None:
    mock_eval_function = MagicMock()

    def simple_eval() -> str:
        mock_eval_function()
        return "eval_result"

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_sync_eval"

        @experiment(pipeline_id="pipeline_sync_eval")
        async def experiment_with_eval() -> str:
            # Simulate @eval decorator by calling register_eval_function directly
            # In real code, @eval would call this.
            register_eval_function(simple_eval)
            return "main_result"

        result = await experiment_with_eval()

        assert result == "main_result"
        mock_start_api.assert_called_once_with(pipelineId="pipeline_sync_eval", name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_sync_eval")
        mock_eval_function.assert_called_once()


@pytest.mark.asyncio
async def test_experiment_with_async_eval_function() -> None:
    mock_async_eval_function = AsyncMock()

    async def simple_async_eval() -> str:
        await mock_async_eval_function()
        return "async_eval_result"

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_async_eval"

        @experiment(pipeline_id="pipeline_async_eval")
        async def experiment_with_async_eval() -> str:
            register_eval_function(simple_async_eval)
            return "main_async_result"

        result = await experiment_with_async_eval()

        assert result == "main_async_result"
        mock_start_api.assert_called_once_with(pipelineId="pipeline_async_eval", name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_async_eval")
        mock_async_eval_function.assert_called_once()


@pytest.mark.asyncio
async def test_experiment_with_multiple_eval_functions() -> None:
    mock_eval1 = MagicMock()
    mock_eval2_async = AsyncMock()

    def sync_eval_1() -> None:
        mock_eval1()

    async def async_eval_2() -> None:
        await mock_eval2_async()

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_multiple_eval"

        @experiment(pipeline_id="pipeline_multiple_eval")
        async def experiment_with_multiple_evals() -> str:
            register_eval_function(sync_eval_1)
            register_eval_function(async_eval_2)
            return "main_multiple_result"

        result = await experiment_with_multiple_evals()

        assert result == "main_multiple_result"
        mock_start_api.assert_called_once_with(pipelineId="pipeline_multiple_eval", name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_multiple_eval")
        mock_eval1.assert_called_once()
        mock_eval2_async.assert_called_once()


@pytest.mark.asyncio
async def test_experiment_eval_function_raises_exception(caplog: LogCaptureFixture) -> None:
    eval_exception = ValueError("Eval failed")

    def faulty_eval() -> None:
        raise eval_exception

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_eval_fail"

        @experiment(pipeline_id="pipeline_eval_fail")
        async def experiment_where_eval_fails() -> str:
            register_eval_function(faulty_eval)
            return "main_result_eval_fail"

        result = await experiment_where_eval_fails()

        assert result == "main_result_eval_fail"

        mock_start_api.assert_called_once_with(pipelineId="pipeline_eval_fail", name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_eval_fail")

        # Check that the error was logged
        assert len(caplog.records) >= 1
        found_log = False
        for record in caplog.records:
            if (
                record.levelname == "ERROR"
                and "@eval function `faulty_eval` encountered an unexpected error. Details: Eval failed"
                in record.message
            ):
                found_log = True
                break
        assert found_log, "Expected error log message not found for faulty_eval"


def test_register_eval_function_outside_experiment_context(caplog: LogCaptureFixture) -> None:
    mock_standalone_eval = MagicMock()

    def standalone_eval_func() -> None:
        mock_standalone_eval()

    assert experiment_module_object.experiment_context_var.get() is None
    assert experiment_module_object._experiment_eval_functions_var.get() is None

    # Clear previous logs if any, and set level to capture WARNING
    caplog.clear()
    caplog.set_level(logging.WARNING)  # Ensure WARNING level is captured

    register_eval_function(standalone_eval_func)

    mock_standalone_eval.assert_not_called()

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == "WARNING"
    assert "The @eval decorator was used on function `standalone_eval_func`" in record.message
    assert "outside of an active @experiment context" in record.message
    assert "This @eval function will not be automatically executed" in record.message


@pytest.mark.asyncio
async def test_experiment_with_mixed_eval_outcomes(caplog: LogCaptureFixture) -> None:
    mock_success_indicator = MagicMock()
    mock_assertion_before_error = MagicMock()
    mock_value_before_error = MagicMock()
    # This mock should not be called as it's after an error in its eval function
    mock_after_error_in_eval = MagicMock()

    def successful_eval() -> str:
        mock_success_indicator()
        return "success"

    def assertion_error_eval() -> None:
        mock_assertion_before_error()
        raise AssertionError("This is a test assertion error")

    async def value_error_eval() -> None:
        mock_value_before_error()
        raise ValueError("This is a test value error")

    caplog.set_level(logging.DEBUG)  # Capture DEBUG and above

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_mixed_outcomes"

        @experiment(pipeline_id="pipeline_mixed_outcomes", options={"name": "MixedTest"})
        async def experiment_with_mixed_evals() -> str:
            register_eval_function(successful_eval)
            register_eval_function(assertion_error_eval)
            register_eval_function(value_error_eval)
            return "main_mixed_result"

        main_result = await experiment_with_mixed_evals()

        assert main_result == "main_mixed_result"
        mock_start_api.assert_called_once_with(pipelineId="pipeline_mixed_outcomes", name="MixedTest", metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_mixed_outcomes")

        mock_success_indicator.assert_called_once()
        mock_assertion_before_error.assert_called_once()
        mock_value_before_error.assert_called_once()
        mock_after_error_in_eval.assert_not_called()

        logs = [(r.levelname, r.message) for r in caplog.records]

        assert ("DEBUG", "Experiment `MixedTest`: Executing 3 registered @eval function(s).") in logs

        assert ("DEBUG", "Executing @eval function: `successful_eval`.") in logs
        assert ("DEBUG", "@eval function `successful_eval` completed successfully.") in logs

        assert ("DEBUG", "Executing @eval function: `assertion_error_eval`.") in logs
        assert (
            "ERROR",
            "@eval function `assertion_error_eval` failed with an AssertionError. Details: This is a test assertion error\nassert False",
        ) in logs

        assert ("DEBUG", "Executing @eval function: `value_error_eval`.") in logs
        assert (
            "ERROR",
            "@eval function `value_error_eval` encountered an unexpected error. Details: This is a test value error",
        ) in logs
