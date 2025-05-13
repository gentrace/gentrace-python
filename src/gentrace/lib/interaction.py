import uuid
from typing import Any, Dict, TypeVar, Callable, Optional, cast

from .traced import traced

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
    the pipeline_id. It preserves the signature of the decorated function
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
        with the interaction tracing logic.

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
        """
        user_provided_attributes = attributes or {}

        # Ensure the SDK-provided pipeline_id attribute takes precedence
        final_attributes = {
            **user_provided_attributes,
            "gentrace.pipeline_id": pipeline_id,
        }

        # The `traced` decorator factory returns a decorator which, when applied to `func` (type F),
        # is known to return a function of type F due to `traced`'s own typing and overloads.
        # However, the factory part of `traced` is typed as returning `Any` for its own overload
        # consistency. We use `cast` here to bridge that inference gap for the type checker.
        actual_traced_decorator = traced(name=name, attributes=final_attributes)
        return cast(F, actual_traced_decorator(func))

    return decorator


__all__ = ["interaction"]
