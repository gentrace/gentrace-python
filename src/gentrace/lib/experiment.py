import contextvars
import functools
import inspect
import sys
from typing import Any, Callable, Coroutine, Dict, Optional, TypeVar

from typing_extensions import TypedDict, ParamSpec

# Placeholder for actual API client functions
# These would typically be part of a Gentrace API client module.

class StartExperimentParamsOptional(TypedDict, total=False):
    metadata: Dict[str, Any]
    name: Optional[str] # If name is also part of start experiment API

class StartExperimentParamsRequired(TypedDict):
    pipelineId: str

class StartExperimentParams(StartExperimentParamsRequired, StartExperimentParamsOptional):
    pass

async def start_experiment_api(params: StartExperimentParams) -> str:
    """Simulates calling the Gentrace API to start an experiment."""
    # In a real implementation, this would make an HTTP request.
    # The name might be passed to the API or only used for the OTEL span.
    print(f"[GENTRACE_DEBUG] API CALL: startExperiment with pipelineId={params['pipelineId']}, metadata={params.get('metadata')}, name={params.get('name')}")
    import uuid
    return str(uuid.uuid4())

class FinishExperimentParams(TypedDict):
    id: str
    # Potentially other fields like status, final_metrics, etc.

async def finish_experiment_api(params: FinishExperimentParams) -> None:
    """Simulates calling the Gentrace API to finish an experiment."""
    # In a real implementation, this would make an HTTP request.
    print(f"[GENTRACE_DEBUG] API CALL: finishExperiment with id={params['id']}")
    pass

P = ParamSpec("P")
R = TypeVar("R")

class ExperimentContext(TypedDict):
    """
    Represents the context for an experiment run. This context is stored in
    a ContextVar to make the experiment ID and pipeline ID available throughout
    the asynchronous execution flow.
    """
    experiment_id: str
    pipeline_id: str

experiment_context_var: contextvars.ContextVar[Optional[ExperimentContext]] = \
    contextvars.ContextVar("gentrace_experiment_context", default=None)

def get_current_experiment_context() -> Optional[ExperimentContext]:
    """
    Retrieves the ExperimentContext (experiment_id, pipeline_id) from the 
    current asynchronous context, if an experiment is active.

    Returns:
        The current ExperimentContext or None if not within an experiment() context.
    """
    return experiment_context_var.get()

class ExperimentOptions(TypedDict, total=False):
    """ Optional parameters for running an experiment. """
    name: Optional[str] 
    """Optional name for the experiment run. This will be used as the name for the root OpenTelemetry span."""
    metadata: Optional[Dict[str, Any]] 
    """User-defined metadata for the experiment. This will be added as attributes to the root OpenTelemetry span."""

def experiment(
    pipeline_id: str,
    options: Optional[ExperimentOptions] = None,
) -> Callable[[Callable[P, Any]], Callable[P, Coroutine[Any, Any, Any]]]:
    """
    A decorator factory that wraps a function to manage a Gentrace Experiment lifecycle.
    This is the primary way to define a scope for running evaluations.

    When a function is decorated with `@experiment`:
    1.  A new Gentrace Experiment run is started by calling the Gentrace API. The optional
        `name` and `metadata` from `options` are passed to this API call.
    2.  The `experiment_id` (obtained from the API) and `pipeline_id` are stored in an
        asynchronous context variable. This context is accessible via
        `get_current_experiment_context()` within the decorated function.
    3.  The primary use of this decorated function is to serve as a context for calling
        evaluation utilities like `eval()` and `eval_dataset()`. These utilities,
        when called within the decorated function, will:
        a.  Access the `experiment_id` and `pipeline_id` from the context.
        b.  Typically create their own OpenTelemetry spans for individual test cases or
            evaluations, tagging these spans with the `experiment_id`.
            (Note: This `@experiment` decorator itself does NOT create an overarching
            OpenTelemetry span for the entire experiment function. OTEL span creation
            is deferred to the evaluation utilities like `eval` or functions
            decorated with `@traced` called within this experiment context).
    4.  If the decorated function is synchronous, it will be run in a way that integrates
        with the surrounding asynchronous operations, and the decorated function will
        become awaitable.
    5.  Upon completion or error of the decorated function, the Gentrace Experiment run is
        finalized via an API call to Gentrace.

    Args:
        pipeline_id: The ID of the pipeline to associate with this experiment.
        options: Optional parameters for the Gentrace Experiment entity:
            name (Optional[str]): A name for the Gentrace Experiment. This is passed to the
                                  Gentrace API.
            metadata (Optional[Dict[str, Any]]): User-defined metadata for the Gentrace Experiment.
                                               Passed to the Gentrace API.

    Returns:
        A decorator that wraps the user's function, transforming it into an awaitable
        that executes the experiment lifecycle logic.

    Usage Example:
        ```python
        from gentrace import experiment, eval, get_current_experiment_context

        @experiment(pipeline_id="my-chatbot-eval-pipeline")
        async def run_my_evaluations():
            # experiment_id is now in context
            print(f"Current experiment context: {get_current_experiment_context()}")

            await eval(
                name="Test Case 1: Greeting",
                inputs={"message": "Hello"},
                expected_output="Hi there!",
                eval_function=my_chatbot_interaction # This function would be @traced or similar
            )
            
            # ... more eval or eval_dataset calls ...
        
        asyncio.run(run_my_evaluations())
        ```
    """

    def inner_decorator(func: Callable[P, Any]) -> Callable[P, Coroutine[Any, Any, Any]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            exp_name_option = options.get("name") if options else None
            user_metadata = options.get("metadata") if options else None

            api_start_params: StartExperimentParams = {"pipelineId": pipeline_id}
            if exp_name_option:
                 api_start_params["name"] = exp_name_option 
            if user_metadata:
                api_start_params["metadata"] = user_metadata # Passed to API
            
            experiment_id_val: Optional[str] = None
            try:
                experiment_id_val = await start_experiment_api(api_start_params)
            except Exception as e:
                print(f"[GENTRACE_ERROR] Failed to start experiment via API: {e}", file=sys.stderr)
                raise

            if not experiment_id_val:
                raise RuntimeError("Failed to obtain experiment_id from API.")

            context_data: ExperimentContext = {
                "experiment_id": experiment_id_val,
                "pipeline_id": pipeline_id,
            }
            
            token = experiment_context_var.set(context_data)
            
            result: Optional[Any] = None

            try:
                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
            except Exception: # Catch all to ensure finally clause runs
                raise
            finally:
                experiment_context_var.reset(token)
                if experiment_id_val: # Check if experiment_id was successfully obtained
                    await finish_experiment_api({"id": experiment_id_val})
            
            return result
        return wrapper
    return inner_decorator

__all__ = ["experiment", "get_current_experiment_context", "ExperimentContext", "ExperimentOptions"] 