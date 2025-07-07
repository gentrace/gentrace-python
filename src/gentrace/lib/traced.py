import inspect
import functools
from typing import Any, Dict, List, TypeVar, Callable, Optional, Coroutine, AsyncGenerator, overload
from typing_extensions import ParamSpec

from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

from .utils import ensure_initialized, _gentrace_json_dumps, gentrace_format_otel_attributes
from .constants import ANONYMOUS_SPAN_NAME, ATTR_GENTRACE_FN_ARGS_EVENT_NAME, ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME

P = ParamSpec("P")
R = TypeVar("R")  # Represents the return type of a sync function, or the awaitable result of an async function
F = TypeVar("F", bound=Callable[..., Any])  # Represents the callable being decorated


@overload
def traced(
    *, name: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


@overload
def traced(
    *, name: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]: ...


@overload
def traced(
    *, name: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None
) -> Callable[[Callable[P, AsyncGenerator[R, None]]], Callable[P, AsyncGenerator[R, None]]]: ...


def traced(*, name: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> Any:
    """
    Wraps a function with OpenTelemetry tracing to track its execution.

    Creates a span for the function execution, records its arguments,
    return value, and any exceptions.

    Args:
        name: Optional custom name for the span. Defaults to the
              function's __name__ or 'anonymous_function'.
        attributes: Optional dictionary of additional attributes to set on the span.
                    These attributes will be prepared for OTLP compatibility.

    Returns:
        A decorator that, when applied to a function, returns a new
        function with tracing enabled.
    """

    final_attributes: Optional[Dict[str, Any]] = None

    if attributes is not None:
        final_attributes = gentrace_format_otel_attributes(attributes)

    def decorator(original_fn: F) -> F:
        resolved_name = name
        if resolved_name is None:
            resolved_name = getattr(original_fn, "__name__", ANONYMOUS_SPAN_NAME)
            if not isinstance(resolved_name, str):
                resolved_name = ANONYMOUS_SPAN_NAME

        actual_span_name: str = resolved_name
        tracer = trace.get_tracer("gentrace")

        if inspect.isasyncgenfunction(original_fn):

            @functools.wraps(original_fn)
            async def async_gen_wrapper(*args: Any, **kwargs: Any) -> AsyncGenerator[Any, None]:
                ensure_initialized()
                with tracer.start_as_current_span(actual_span_name, attributes=final_attributes) as span:
                    try:
                        sig = inspect.signature(original_fn)
                        bound_arguments = sig.bind(*args, **kwargs).arguments
                        transformed_arguments = [{k: v} for k, v in bound_arguments.items()]
                        serialized_inputs = _gentrace_json_dumps(transformed_arguments)
                        span.add_event(
                            ATTR_GENTRACE_FN_ARGS_EVENT_NAME,
                            {"args": serialized_inputs},
                        )

                        result_list: List[Any] = []
                        # original_fn is F, which in this branch is an async generator function.
                        # The result of calling it is an async generator.
                        async for item in original_fn(*args, **kwargs):
                            result_list.append(item)
                            yield item

                        serialized_result = _gentrace_json_dumps(result_list)
                        span.add_event(ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME, {"output": serialized_result})

                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, description=str(e)))
                        span.set_attribute("error.type", e.__class__.__name__)
                        raise

            return async_gen_wrapper  # type: ignore[return-value]

        elif inspect.iscoroutinefunction(original_fn):

            @functools.wraps(original_fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                ensure_initialized()
                with tracer.start_as_current_span(actual_span_name, attributes=final_attributes) as span:
                    try:
                        sig = inspect.signature(original_fn)
                        bound_arguments = sig.bind(*args, **kwargs).arguments

                        # Transform the arguments dictionary into a list of single-key dictionaries
                        transformed_arguments = [{k: v} for k, v in bound_arguments.items()]
                        serialized_inputs = _gentrace_json_dumps(transformed_arguments)

                        span.add_event(
                            ATTR_GENTRACE_FN_ARGS_EVENT_NAME,
                            {"args": serialized_inputs},
                        )
                        # original_fn is F, which in this branch is Callable[P, Coroutine[Any, Any, R]]
                        # The result of awaiting it is R.
                        result = await original_fn(*args, **kwargs)

                        serialized_result = _gentrace_json_dumps(result)

                        span.add_event(ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME, {"output": serialized_result})
                        return result
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, description=str(e)))
                        span.set_attribute("error.type", e.__class__.__name__)
                        raise

            # The `async_wrapper` is typed as returning `Any` for internal simplicity.
            # However, due to `@functools.wraps` and the `iscoroutinefunction` check,
            # it correctly matches the signature of `original_fn` (type `F`).
            # We ignore the type checker's complaint about returning `Any` when `F` is expected.
            return async_wrapper  # type: ignore[return-value]
        else:

            @functools.wraps(original_fn)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                ensure_initialized()
                with tracer.start_as_current_span(actual_span_name) as span:
                    if final_attributes:
                        span.set_attributes(final_attributes)

                    try:
                        sig = inspect.signature(original_fn)
                        bound_arguments = sig.bind(*args, **kwargs).arguments

                        # Transform the arguments dictionary into a list of single-key dictionaries
                        transformed_arguments = [{k: v} for k, v in bound_arguments.items()]
                        serialized_inputs = _gentrace_json_dumps(transformed_arguments)

                        span.add_event(
                            ATTR_GENTRACE_FN_ARGS_EVENT_NAME,
                            {"args": serialized_inputs},
                        )
                        # original_fn is F, which in this branch is Callable[P, R]
                        # The result of calling it is R.
                        result = original_fn(*args, **kwargs)

                        serialized_result = _gentrace_json_dumps(result)

                        span.add_event(ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME, {"output": serialized_result})
                        return result
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, description=str(e)))
                        span.set_attribute("error.type", e.__class__.__name__)
                        raise

            # The `sync_wrapper` is typed as returning `Any` for internal simplicity.
            # However, due to `@functools.wraps`, it correctly matches the
            # signature of `original_fn` (type `F`). We ignore the type checker's
            # complaint about returning `Any` when `F` is expected.
            return sync_wrapper  # type: ignore[return-value]

    return decorator
