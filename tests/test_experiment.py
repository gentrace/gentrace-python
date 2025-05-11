import sys
from unittest.mock import patch, AsyncMock, MagicMock
import logging

import pytest
from pytest import LogCaptureFixture

from gentrace.lib.experiment import (
    experiment,
    get_current_experiment_context, # Will be used later
    # ExperimentContext, # Will be used later
    ExperimentOptions,
    # register_eval_function, # REMOVED
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
        mock_start_api.assert_called_once_with(
            pipelineId="test_pipeline", name=None, metadata=None
        )
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
        mock_start_api.assert_called_once_with(
            pipelineId="test_pipeline_sync", name=None, metadata=None
        )
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

        mock_start_api.assert_called_once_with(
            pipelineId="pipeline_for_context", name=None, metadata=None
        )
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

        mock_start_api.assert_called_once_with(
            pipelineId="pipeline_api_fail", name=None, metadata=None
        )
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

        @experiment(pipeline_id="pipeline_sync_eval")
        async def experiment_with_eval() -> str:
            simple_eval_like_function() # Directly call the function
            return "main_result"

        result = await experiment_with_eval()

        assert result == "main_result"
        mock_start_api.assert_called_once_with(
            pipelineId="pipeline_sync_eval", name=None, metadata=None
        )
        mock_finish_api.assert_called_once_with(id="exp_id_sync_eval")
        mock_eval_function.assert_called_once()


@pytest.mark.asyncio
async def test_experiment_with_called_async_function() -> None:
    mock_async_eval_function = AsyncMock()

    # This function would conceptually be decorated with @eval in real usage
    async def simple_async_eval_like_function() -> str:
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
            await simple_async_eval_like_function() # Directly call and await
            return "main_async_result"

        result = await experiment_with_async_eval()

        assert result == "main_async_result"
        mock_start_api.assert_called_once_with(
            pipelineId="pipeline_async_eval", name=None, metadata=None
        )
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

        @experiment(pipeline_id="pipeline_multiple_eval")
        async def experiment_with_multiple_evals() -> str:
            sync_eval_1()
            await async_eval_2()
            return "main_multiple_result"

        result = await experiment_with_multiple_evals()

        assert result == "main_multiple_result"
        mock_start_api.assert_called_once_with(
            pipelineId="pipeline_multiple_eval", name=None, metadata=None
        )
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

        @experiment(pipeline_id="pipeline_eval_fail")
        async def experiment_where_internal_call_fails() -> str:
            # The exception from faulty_function_called_in_experiment will propagate
            # and be caught by the test's `pytest.raises` or by pytest itself if unhandled.
            faulty_function_called_in_experiment()
            return "main_result_eval_fail" # This won't be reached

        # The experiment decorator itself doesn't catch exceptions from the user's code,
        # it ensures finish_experiment_api is called in a finally block.
        with pytest.raises(ValueError, match="Eval failed"):
            await experiment_where_internal_call_fails()
        
        # finish_experiment_api should still be called due to the finally block
        mock_start_api.assert_called_once_with(
            pipelineId="pipeline_eval_fail", name=None, metadata=None
        )
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
        assert False, "This is a test assertion error"
        # Code after assert False won't run

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

        @experiment(pipeline_id="pipeline_mixed_outcomes", options={"name": "MixedTest"})
        async def experiment_with_mixed_calls() -> str:
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
            return "main_mixed_result"

        main_result = await experiment_with_mixed_calls()

        assert main_result == "main_mixed_result"
        mock_start_api.assert_called_once_with(
            pipelineId="pipeline_mixed_outcomes", name="MixedTest", metadata=None
        )
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