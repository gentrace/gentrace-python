import uuid
import inspect
import functools
from typing import Any, Dict, TypeVar, Callable, Optional, cast

from opentelemetry import baggage as otel_baggage, context as otel_context

from .traced import traced
from .constants import ATTR_GENTRACE_SAMPLE_KEY, ATTR_GENTRACE_PIPELINE_ID

F = TypeVar("F", bound=Callable[..., Any])


def interaction(
    *,
    pipeline_id: str,
    name: Optional[str] = None,
    attributes: Optional[Dict[str, Any]] = None,
) -> Callable[[F], F]:
    """
    A decorator factory that wraps a function with OpenTelemetry tracing to track
    interactions within a Gentrace pipeline.

    This decorator leverages the @traced decorator for core tracing logic and
    adds specific attributes related to the Gentrace interaction, such as
    the pipeline_id. It also sets 'gentrace.sample'="true" in the OpenTelemetry
    baggage for the duration of the traced function's execution.
    It preserves the signature of the decorated function
    and supports both synchronous and asynchronous functions.

    Args:
        pipeline_id: The identifier of the pipeline this interaction belongs to.
                     This will be added as an attribute 'gentrace.pipeline_id' to the span.
                     Must be a valid UUID string.
        name: Optional. A custom name for the OpenTelemetry span. If not provided,
              the name will default to the decorated function's __name__ or
              ANONYMOUS_SPAN_NAME (as handled by the underlying @traced decorator).
        attributes: Optional. A dictionary of additional attributes to set on the span.
                    These will be merged with the 'gentrace.pipeline_id' attribute.

    Returns:
        A decorator that, when applied to a function, returns a new function
        with the interaction tracing and baggage modification logic.

    Usage:
        @interaction(pipeline_id="example-pipeline")
        def process_data(data):
            return f"Processed {data}"

        @interaction(pipeline_id="async-pipeline", name="custom_async_interaction")
        async def fetch_remote_data(url):
            # async http call
            return await fetch(url)
    """

    try:
        uuid.UUID(pipeline_id)
    except ValueError as e:
        raise ValueError(
            f"Attribute 'gentrace.pipeline_id' must be a valid UUID string. Received: '{pipeline_id}'"
        ) from e

    def decorator(func: F) -> F:
        """
        The actual decorator that takes the function to be wrapped.
        It applies baggage modification and then the @traced decorator.
        """
        user_provided_span_attributes = attributes or {}
        # Attributes for the span created by @traced
        final_span_attributes_for_traced = {
            **user_provided_span_attributes,
            ATTR_GENTRACE_PIPELINE_ID: pipeline_id,
        }

        configured_traced_decorator = traced(name=name, attributes=final_span_attributes_for_traced)

        func_instrumented_by_traced = configured_traced_decorator(func)

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def baggage_context_wrapper_async(*args: Any, **kwargs: Any) -> Any:
                current_context = otel_context.get_current()
                context_with_modified_baggage = otel_baggage.set_baggage(
                    ATTR_GENTRACE_SAMPLE_KEY, "true", context=current_context
                )

                token = otel_context.attach(context_with_modified_baggage)
                try:
                    return await func_instrumented_by_traced(*args, **kwargs)
                finally:
                    otel_context.detach(token)

            return cast(F, baggage_context_wrapper_async)
        else:

            @functools.wraps(func)
            def baggage_context_wrapper_sync(*args: Any, **kwargs: Any) -> Any:
                current_context = otel_context.get_current()
                context_with_modified_baggage = otel_baggage.set_baggage(
                    ATTR_GENTRACE_SAMPLE_KEY, "true", context=current_context
                )

                token = otel_context.attach(context_with_modified_baggage)
                try:
                    return func_instrumented_by_traced(*args, **kwargs)
                finally:
                    otel_context.detach(token)

            return cast(F, baggage_context_wrapper_sync)

    return decorator


__all__ = ["interaction"]
