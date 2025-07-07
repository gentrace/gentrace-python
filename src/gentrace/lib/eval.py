import inspect
import logging
import warnings
import functools
from typing import Any, Dict, TypeVar, Callable, Optional, Coroutine, cast
from typing_extensions import ParamSpec

from opentelemetry import trace, baggage as otel_baggage, context as otel_context
from opentelemetry.trace.status import Status, StatusCode

from .utils import ensure_initialized, _gentrace_json_dumps
from .constants import (
    ANONYMOUS_SPAN_NAME,
    ATTR_GENTRACE_SAMPLE_KEY,
    ATTR_GENTRACE_EXPERIMENT_ID,
    ATTR_GENTRACE_TEST_CASE_NAME,
    ATTR_GENTRACE_FN_ARGS_EVENT_NAME,
    ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME,
)
from .experiment import ExperimentContext, get_current_experiment_context

P = ParamSpec("P")
R = TypeVar("R")

_tracer = trace.get_tracer("gentrace.sdk")
logger = logging.getLogger("gentrace")

RESERVED_METADATA_KEYS = {
    ATTR_GENTRACE_EXPERIMENT_ID,
    ATTR_GENTRACE_TEST_CASE_NAME,
    ATTR_GENTRACE_FN_ARGS_EVENT_NAME,
    ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME,
}


# Implementation signature: Accepts any callable, returns generic async wrapper
def eval(
    *,
    name: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable[[Callable[P, Any]], Callable[P, Coroutine[Any, Any, Any]]]:  # Input Any, output Any
    """
    Decorator factory to mark a function as a single evaluation test case within an experiment.

    This decorator must be used on a function that is then called directly from within the
    scope of an `@experiment()` decorated function.

    When the decorated function is called:
    1. It retrieves the current `experiment_id` and `pipeline_id` from the context
       set by `@experiment()`.
    2. It creates an OpenTelemetry span representing this specific evaluation.
       The span is named using the provided `name` argument.
    3. Attributes `gentrace.experiment_id` and `gentrace.test_case_name` are set on the span.
    4. Any provided `metadata` is added to the span.
    5. The decorated function's execution (inputs, output, errors) is captured within this span:
       - Input arguments are logged as a 'gentrace.fn.args' event with an 'args' key
       - Function output is logged as a 'gentrace.fn.output' event with an 'output' key
    6. If the decorated function is synchronous, it is wrapped to be awaitable, fitting into
       the common asynchronous flow of experiment execution. The returned awaitable yields
       the original synchronous function's return value.

    Args:
        name: A descriptive name for this evaluation test case. This will be used as part
              of the OTEL span name and as an attribute (gentrace.test_case_name).
        metadata: Optional dictionary of arbitrary metadata to attach to this evaluation's span.

    Returns:
        A decorator that wraps the user's function. The wrapped function, when called,
        will execute the evaluation logic.
    """

    # Inner decorator matches implementation signature
    def inner_decorator(func: Callable[P, Any]) -> Callable[P, Coroutine[Any, Any, Any]]:
        # Wrapper is async, return type Any matches inner_decorator
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            ensure_initialized()
            experiment_context: Optional[ExperimentContext] = get_current_experiment_context()

            if not experiment_context:
                func_name = getattr(func, "__name__", ANONYMOUS_SPAN_NAME)
                raise RuntimeError(
                    f"@eval(name='{name}') on function '{func_name}' must be called within an active @experiment context."
                )

            span_name = name

            # Set up baggage context similar to @interaction()
            current_context = otel_context.get_current()
            context_with_modified_baggage = otel_baggage.set_baggage(
                ATTR_GENTRACE_SAMPLE_KEY, "true", context=current_context
            )

            token = otel_context.attach(context_with_modified_baggage)
            try:
                with _tracer.start_as_current_span(span_name) as span:
                    span.set_attribute(ATTR_GENTRACE_EXPERIMENT_ID, experiment_context["experiment_id"])
                    span.set_attribute(ATTR_GENTRACE_TEST_CASE_NAME, span_name)  # Use eval name for test case name

                    if metadata:
                        for key, value in metadata.items():
                            if key in RESERVED_METADATA_KEYS:
                                warnings.warn(
                                    f"Metadata key `{key}` is reserved and will be ignored for @eval test case `{name}`. Avoid using reserved keys for metadata.",
                                    UserWarning,
                                    stacklevel=2,
                                )
                                continue
                            try:
                                # Attempt to serialize complex types, fallback to string
                                if isinstance(value, (dict, list, tuple)):
                                    span.set_attribute(key, _gentrace_json_dumps(value))
                                elif value is not None:
                                    span.set_attribute(key, str(value))
                                # None values are implicitly ignored by set_attribute
                            except TypeError:  # Catch serialization errors specifically
                                logger.warning(
                                    f"Metadata value for key `{key}` is not serializable for span attributes. Storing as string.",
                                    exc_info=True,
                                )
                                span.set_attribute(key, f"[Unserializable value for {key}]")
                            except Exception as e:  # Catch any other unexpected errors during attribute setting
                                logger.error(f"Unexpected error setting metadata attribute {key}: {e}", exc_info=True)
                                span.set_attribute(key, f"[Error setting metadata: {key}]")

                    # Combine args and kwargs for logging
                    input_payload: Dict[str, Any] = {}
                    if args:
                        # Use repr for args to handle non-serializable objects gracefully
                        input_payload["args"] = [repr(a) for a in args]
                    if kwargs:
                        # Use repr for kwargs values
                        input_payload["kwargs"] = {k: repr(v) for k, v in kwargs.items()}

                    if input_payload:
                        # Log combined args/kwargs if any exist
                        span.add_event(ATTR_GENTRACE_FN_ARGS_EVENT_NAME, {"args": _gentrace_json_dumps(input_payload)})

                    try:
                        if inspect.iscoroutinefunction(func):
                            # The cast isn't strictly needed runtime but clarifies intent for readers/linters
                            async_func = cast(Callable[P, Coroutine[Any, Any, Any]], func)
                            result = await async_func(*args, **kwargs)
                        else:
                            # func is already Callable[P, Any], no cast needed for sync_func
                            result = func(*args, **kwargs)  # Directly use func

                        span.add_event(ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME, {"output": _gentrace_json_dumps(result)})
                        return result  # Runtime result is correct type, static type is Any
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, description=str(e)))
                        span.set_attribute("error.type", e.__class__.__name__)
                        raise
            finally:
                otel_context.detach(token)

        return wrapper

    return inner_decorator


__all__ = ["eval"]
