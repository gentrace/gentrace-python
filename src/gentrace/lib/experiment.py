import uuid
import inspect
import logging
import functools
import contextvars
from typing import Any, Dict, Union, TypeVar, Callable, Optional, Awaitable, Coroutine
from typing_extensions import ParamSpec, TypedDict

from .utils import ensure_initialized
from .client_instance import _get_async_client_instance
from ..types.experiment import Experiment
from .experiment_control import start_experiment_api, finish_experiment_api

P = ParamSpec("P")
R = TypeVar("R")

logger = logging.getLogger("gentrace")


class ExperimentContext(TypedDict):
    """
    Represents the context for an experiment run. This context is stored in
    a ContextVar to make the experiment ID, pipeline ID, and URL available throughout
    the asynchronous execution flow.
    """

    experiment_id: str
    pipeline_id: str
    experiment_url: Optional[str]  # URL to view the experiment in the Gentrace UI


experiment_context_var: contextvars.ContextVar[Optional[ExperimentContext]] = contextvars.ContextVar(
    "gentrace_experiment_context", default=None
)


def get_current_experiment_context() -> Optional[ExperimentContext]:
    """
    Retrieves the ExperimentContext (experiment_id, pipeline_id) from the
    current asynchronous context, if an experiment is active.

    Returns:
        The current ExperimentContext or None if not within an experiment() context.
    """
    return experiment_context_var.get()


class ExperimentOptions(TypedDict, total=False):
    """Optional parameters for running an experiment."""

    name: Optional[str]
    """Optional name for the experiment run. This will be used as the name for the root OpenTelemetry span."""
    metadata: Optional[Dict[str, Any]]
    """User-defined metadata for the experiment. This will be added as attributes to the root OpenTelemetry span."""


class ExperimentResult(Experiment):
    """The result of an experiment run, containing all experiment fields plus the URL."""
    
    url: str
    """Full URL to view the experiment in the Gentrace UI"""


def experiment(
    *,
    pipeline_id: Optional[str] = None,
    options: Optional[ExperimentOptions] = None,
) -> Callable[[Callable[P, Any]], Callable[P, Coroutine[Any, Any, ExperimentResult]]]:
    """
    A decorator factory that wraps a function to manage a Gentrace Experiment lifecycle.
    This is the primary way to define a scope for running evaluations. The decorated
    function's return value is ignored. The call to the decorated function will
    resolve to an ExperimentResult containing the experiment details and URL.

    When a function is decorated with `@experiment`:
    1.  A new Gentrace Experiment run is started by calling the Gentrace API. The optional
        `name` and `metadata` from `options` are passed to this API call.
    2.  The `experiment_id` (obtained from the API) and `pipeline_id` are stored in an
        asynchronous context variable. This context is accessible via
        `get_current_experiment_context()` within the decorated function.
    3.  The primary use of this decorated function is to serve as a context for calling
        evaluation functions (e.g., those decorated with `@eval`) or other tracing utilities
        like `eval_dataset()`. These utilities, when called within the decorated function, will:
        a.  Access the `experiment_id` and `pipeline_id` from the context.
        b.  Typically create their own OpenTelemetry spans for individual test cases or
            evaluations, tagging these spans with the `experiment_id`.
            (Note: This `@experiment` decorator itself does NOT create an overarching
            OpenTelemetry span for the entire experiment function. OTEL span creation
            is deferred to the evaluation utilities or functions
            decorated with `@traced` called within this experiment context).
    4.  If the decorated function is synchronous, it will be run in a way that integrates
        with the surrounding asynchronous operations, and the decorated function will
        become awaitable.
    5.  Upon completion or error of the decorated function, the Gentrace Experiment run is
        finalized via an API call to Gentrace.
    6.  Any value returned by the decorated function is ignored. The decorated function,
        when called, will return an ExperimentResult containing the experiment details
        and a URL to view the experiment in the Gentrace UI.

    Args:
        pipeline_id: The ID of the pipeline to associate with this experiment.
                     If not provided, defaults to 'default'.
        options: Optional parameters for the Gentrace Experiment entity:
            name (Optional[str]): A name for the Gentrace Experiment. This is passed to the
                                  Gentrace API.
            metadata (Optional[Dict[str, Any]]): User-defined metadata for the Gentrace Experiment.
                                               Passed to the Gentrace API.

    Returns:
        A decorator that wraps the user's function, transforming it into an awaitable
        that executes the experiment lifecycle logic and resolves to an ExperimentResult.

    Usage Example:
        ```python
        from gentrace import experiment, eval, compose_email
        import asyncio


        @experiment(pipeline_id="<your-pipeline-id>")
        async def email_evals_experiment():
            @eval(name="check_subject_and_body_1")
            async def check_email_content_1(subject_to_check: str, body_to_check: str):
                email = compose_email(
                    subject=subject_to_check,
                    body=body_to_check,
                    to="test@example.com",
                    from_="test@example.com",
                )
                assert subject_to_check in email
                assert body_to_check in email
                return email

            # Invoke the @eval decorated function immediately after definition
            await check_email_content_1(subject_to_check="Hello Test", body_to_check="This is a test email.")

            @eval(name="check_subject_and_body_2")
            async def check_email_content_2(subject_to_check: str, body_to_check: str):
                email = compose_email(
                    subject=subject_to_check,
                    body=body_to_check,
                    to="test@example.com",
                    from_="test@example.com",
                )
                assert subject_to_check in email
                assert body_to_check in email
                return email

            # Invoke again, perhaps with different params or as a separate test case
            await check_email_content_2(subject_to_check="Another Subject", body_to_check="Another body.")


        # To run the experiment:
        # asyncio.run(email_evals_experiment())
        ```
    """

    # Use 'default' if no pipeline_id is provided
    effective_pipeline_id = pipeline_id if pipeline_id is not None else 'default'
    
    # Validate UUID format (skip validation for 'default')
    if effective_pipeline_id != 'default':
        try:
            uuid.UUID(effective_pipeline_id)
        except ValueError as e:
            raise ValueError(f"Invalid pipeline_id: '{effective_pipeline_id}'. Must be a valid UUID.") from e

    def inner_decorator(func: Callable[P, Union[None, Awaitable[None]]]) -> Callable[P, Coroutine[Any, Any, ExperimentResult]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> ExperimentResult:
            ensure_initialized()
            exp_name_option = options.get("name") if options else None
            user_metadata = options.get("metadata") if options else None

            experiment_obj: Optional[Experiment] = None
            try:
                experiment_obj = await start_experiment_api(
                    pipelineId=effective_pipeline_id, name=exp_name_option, metadata=user_metadata
                )
            except Exception as e:
                logger.error(f"Failed to start Gentrace experiment via API. Details: {e}")
                raise

            if not experiment_obj:
                raise RuntimeError("Failed to obtain experiment from API.")

            # Construct the experiment URL early so it can be displayed immediately
            # Get the client to access base_url
            client = _get_async_client_instance()
            base_url = str(client.base_url).rstrip('/')
            
            # Extract hostname from base URL (remove /api suffix if present)
            if base_url.endswith('/api'):
                hostname = base_url[:-4]
            else:
                hostname = base_url
            
            # Construct the URL using resource_path
            experiment_url = f"{hostname}{experiment_obj.resource_path}"

            context_data: ExperimentContext = {
                "experiment_id": experiment_obj.id,
                "pipeline_id": effective_pipeline_id,
                "experiment_url": experiment_url,
            }

            token = experiment_context_var.set(context_data)

            try:
                if inspect.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    func(*args, **kwargs)

            finally:
                experiment_context_var.reset(token)
                if experiment_obj:
                    await finish_experiment_api(id=experiment_obj.id)

            # Create ExperimentResult instance with all fields from experiment plus URL
            # Use model_dump with by_alias=True to get camelCase field names
            experiment_data = experiment_obj.model_dump(by_alias=True)
            
            result = ExperimentResult(
                **experiment_data,
                url=experiment_url  # Use the URL we constructed earlier
            )
            
            return result

        return wrapper

    return inner_decorator


__all__ = ["experiment", "get_current_experiment_context", "ExperimentContext", "ExperimentOptions", "ExperimentResult"]
