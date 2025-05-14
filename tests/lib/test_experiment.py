import sys
import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest import LogCaptureFixture

from gentrace.lib.experiment import (
    # ExperimentContext, # Will be used later
    ExperimentOptions,
    # register_eval_function, # REMOVED
    experiment,
    get_current_experiment_context,  # Will be used later
)

# Get a direct reference to the module where experiment() is defined
experiment_module_object = sys.modules["gentrace.lib.experiment"]

PIPELINE_ID = "04b20fda-dbbe-4849-a927-3906fe743ef5"


@pytest.mark.asyncio
async def test_experiment_decorator_simple_async_function() -> None:
    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "test_experiment_id"

        @experiment(pipeline_id=PIPELINE_ID)
        async def sample_async_function() -> None:
            pass

        await sample_async_function()

        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="test_experiment_id")


@pytest.mark.asyncio
async def test_experiment_decorator_simple_sync_function() -> None:
    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "test_experiment_id_sync"

        @experiment(pipeline_id=PIPELINE_ID)
        def sample_sync_function() -> None:
            pass

        # Even though sample_sync_function is sync, the decorator makes it awaitable
        await sample_sync_function()

        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="test_experiment_id_sync")


@pytest.mark.asyncio
async def test_experiment_context_is_set_and_retrievable() -> None:
    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_context_test"

        @experiment(pipeline_id=PIPELINE_ID)
        async def function_with_context_check() -> None:
            context = get_current_experiment_context()
            assert context is not None
            assert context["experiment_id"] == "exp_id_context_test"
            assert context["pipeline_id"] == PIPELINE_ID

            # Check context variable directly too
            raw_context = experiment_module_object.experiment_context_var.get()
            assert raw_context is not None
            assert raw_context["experiment_id"] == "exp_id_context_test"
            assert raw_context["pipeline_id"] == PIPELINE_ID

        await function_with_context_check()

        # Context should be reset outside the function
        assert experiment_module_object.experiment_context_var.get() is None
        assert get_current_experiment_context() is None

        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name=None, metadata=None)
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

        @experiment(pipeline_id=PIPELINE_ID, options=options)
        async def function_with_options() -> None:
            pass

        await function_with_options()

        mock_start_api.assert_called_once_with(
            pipelineId=PIPELINE_ID,
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

        @experiment(pipeline_id=PIPELINE_ID)
        async def function_where_api_fails() -> None:
            pass

        with pytest.raises(ValueError, match="API start failed"):
            await function_where_api_fails()

        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name=None, metadata=None)
        mock_finish_api.assert_not_called()
        # Context should not be set if start_api failed before setting it
        assert experiment_module_object.experiment_context_var.get() is None


@pytest.mark.asyncio
async def test_experiment_with_called_sync_function() -> None:
    mock_eval_function = MagicMock()

    # This function would conceptually be decorated with @eval in real usage
    def simple_eval_like_function() -> str:
        mock_eval_function()
        return "eval_result"

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_sync_eval"

        @experiment(pipeline_id=PIPELINE_ID)
        async def experiment_with_eval() -> None:
            simple_eval_like_function()  # Directly call the function
            pass

        await experiment_with_eval()

        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_sync_eval")
        mock_eval_function.assert_called_once()


@pytest.mark.asyncio
async def test_experiment_with_called_async_function() -> None:
    mock_async_eval_function = AsyncMock()

    # This function would conceptually be decorated with @eval in real usage
    async def simple_async_eval_like_function() -> None:
        await mock_async_eval_function()

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_async_eval"

        @experiment(pipeline_id=PIPELINE_ID)
        async def experiment_with_async_eval() -> None:
            await simple_async_eval_like_function()  # Directly call and await
            pass

        await experiment_with_async_eval()

        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_async_eval")
        mock_async_eval_function.assert_called_once()


@pytest.mark.asyncio
async def test_experiment_with_multiple_called_functions() -> None:
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

        @experiment(pipeline_id=PIPELINE_ID)
        async def experiment_with_multiple_evals() -> None:
            sync_eval_1()
            await async_eval_2()

        await experiment_with_multiple_evals()

        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_multiple_eval")
        mock_eval1.assert_called_once()
        mock_eval2_async.assert_called_once()


@pytest.mark.asyncio
async def test_experiment_called_function_raises_exception() -> None:
    eval_exception = ValueError("Eval failed")

    # This function would be decorated with @eval in real use.
    # The @eval decorator would handle exception recording.
    # For this test, we just care the experiment finishes.
    def faulty_function_called_in_experiment() -> None:
        raise eval_exception

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_eval_fail"

        @experiment(pipeline_id=PIPELINE_ID)
        async def experiment_where_internal_call_fails() -> None:
            # The exception from faulty_function_called_in_experiment will propagate
            # and be caught by the test's `pytest.raises` or by pytest itself if unhandled.
            faulty_function_called_in_experiment()

        # The experiment decorator itself doesn't catch exceptions from the user's code,
        # it ensures finish_experiment_api is called in a finally block.
        with pytest.raises(ValueError, match="Eval failed"):
            await experiment_where_internal_call_fails()

        # finish_experiment_api should still be called due to the finally block
        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name=None, metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_eval_fail")

        # No specific logging from @experiment about @eval errors anymore
        # Assertions about specific @eval error logs are removed.
        # If @eval itself logs, that would be separate.


# Removed test_register_eval_function_outside_experiment_context as it's no longer applicable


@pytest.mark.asyncio
async def test_experiment_with_mixed_outcomes_in_called_functions(caplog: LogCaptureFixture) -> None:
    mock_success_indicator = MagicMock()
    mock_assertion_before_error = MagicMock()

    # This function would be @eval decorated
    def successful_called_func() -> str:
        mock_success_indicator()
        return "success"

    # This function would be @eval decorated. The @eval decorator would handle the AssertionError.
    def assertion_error_called_func() -> None:
        mock_assertion_before_error()
        raise AssertionError("This is a test assertion error")

    # This function would be @eval decorated. The @eval decorator would handle the ValueError.
    async def value_error_called_func() -> None:
        raise ValueError("This is a test value error")

    caplog.set_level(logging.DEBUG)

    with patch.object(
        experiment_module_object, "start_experiment_api", new_callable=AsyncMock
    ) as mock_start_api, patch.object(
        experiment_module_object, "finish_experiment_api", new_callable=AsyncMock
    ) as mock_finish_api:
        mock_start_api.return_value = "exp_id_mixed_outcomes"

        @experiment(pipeline_id=PIPELINE_ID, options={"name": "MixedTest"})
        async def experiment_with_mixed_calls() -> None:
            successful_called_func()

            try:
                assertion_error_called_func()
            except AssertionError:
                # In a real scenario with @eval, @eval's wrapper would catch this.
                # Here, the experiment itself doesn't catch it, so the test needs to
                # simulate that the error is handled by simply passing, allowing the experiment to continue.
                pass

            try:
                await value_error_called_func()
            except ValueError:
                # Similar to above, @eval would handle, experiment doesn't.
                pass

        await experiment_with_mixed_calls()

        mock_start_api.assert_called_once_with(pipelineId=PIPELINE_ID, name="MixedTest", metadata=None)
        mock_finish_api.assert_called_once_with(id="exp_id_mixed_outcomes")

        mock_success_indicator.assert_called_once()
        mock_assertion_before_error.assert_called_once()

        # Logging assertions about "Executing @eval function" are removed as that mechanism is gone.
        # Any logging would now come from the @eval decorator itself when the functions are called.
        # This test primarily focuses on the @experiment decorator's behavior.

        # Example: if @eval logs something specific, we could check for that.
        # For now, we confirm the experiment completes and the main mocks are called.
        initial_log_messages = [r.message for r in caplog.records]
        assert not any("Executing @eval function:" in msg for msg in initial_log_messages)
        assert not any("Experiment `MixedTest`: Executing" in msg for msg in initial_log_messages)
