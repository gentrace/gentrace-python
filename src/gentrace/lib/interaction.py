import uuid
import inspect
import functools
from typing import Any, Dict, TypeVar, Callable, Optional, AsyncGenerator, cast

from opentelemetry import baggage as otel_baggage, context as otel_context

from .utils import ensure_initialized, display_pipeline_error
from .traced import traced
from .constants import ATTR_GENTRACE_SAMPLE_KEY, ATTR_GENTRACE_PIPELINE_ID
from .validation import start_pipeline_validation

F = TypeVar("F", bound=Callable[..., Any])





def interaction(
    *,
    pipeline_id: Optional[str] = None,
    name: Optional[str] = None,
    attributes: Optional[Dict[str, Any]] = None,
    suppress_warnings: bool = False,
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
        pipeline_id: Optional. The identifier of the pipeline this interaction belongs to.
                     If not provided, defaults to "default" which will use the organization's 
                     default pipeline. This will be added as an attribute 'gentrace.pipeline_id' 
                     to the span. When provided, must be a valid UUID string.
        name: Optional. A custom name for the OpenTelemetry span. If not provided,
              the name will default to the decorated function's __name__ or
              ANONYMOUS_SPAN_NAME (as handled by the underlying @traced decorator).
        attributes: Optional. A dictionary of additional attributes to set on the span.
                    These will be merged with the 'gentrace.pipeline_id' attribute.
        suppress_warnings: Optional. If True, suppresses auto-initialization warnings.
                          Defaults to False.

    Returns:
        A decorator that, when applied to a function, returns a new function
        with the interaction tracing and baggage modification logic.

    Usage:
        # Simplest usage - uses default pipeline
        @interaction()
        def process_data(data):
            return f"Processed {data}"
        
        # With custom attributes but no pipeline ID
        @interaction(attributes={"model": "gpt-4", "temperature": 0.7})
        def process_with_attrs(data):
            return f"Processed {data}"

        # Explicit pipeline ID (backward compatible)
        @interaction(pipeline_id="example-pipeline")
        def process_explicit(data):
            return f"Processed {data}"

        # Async function with custom name
        @interaction(pipeline_id="async-pipeline", name="custom_async_interaction")
        async def fetch_remote_data(url):
            # async http call
            return await fetch(url)
    """
    
    # Use 'default' if no pipeline_id is provided
    effective_pipeline_id = pipeline_id if pipeline_id is not None else 'default'

    # Validate UUID format (skip validation for 'default')
    is_valid_uuid = True
    if effective_pipeline_id != 'default':
        try:
            uuid.UUID(effective_pipeline_id)
        except ValueError:
            is_valid_uuid = False
            display_pipeline_error(effective_pipeline_id, 'invalid-format')
    
    # Start pipeline validation in background if UUID is valid and not 'default'
    if is_valid_uuid and effective_pipeline_id != 'default':
        # Ensure Gentrace is initialized before validation
        ensure_initialized(suppress_warnings=suppress_warnings)
        
        # Start validation in the background
        start_pipeline_validation(effective_pipeline_id)

    def decorator(func: F) -> F:
        """
        The actual decorator that takes the function to be wrapped.
        It applies baggage modification and then the @traced decorator.
        """
        user_provided_span_attributes = attributes or {}
        # Attributes for the span created by @traced
        final_span_attributes_for_traced = {
            **user_provided_span_attributes,
            ATTR_GENTRACE_PIPELINE_ID: effective_pipeline_id,
        }

        configured_traced_decorator = traced(name=name, attributes=final_span_attributes_for_traced)

        func_instrumented_by_traced = configured_traced_decorator(func)

        if inspect.isasyncgenfunction(func):

            @functools.wraps(func)
            async def baggage_context_wrapper_async_gen(*args: Any, **kwargs: Any) -> AsyncGenerator[Any, None]:
                # Ensure Gentrace is initialized (auto-init if possible)
                ensure_initialized(suppress_warnings=suppress_warnings)
                
                current_context = otel_context.get_current()
                context_with_modified_baggage = otel_baggage.set_baggage(
                    ATTR_GENTRACE_SAMPLE_KEY, "true", context=current_context
                )

                token = otel_context.attach(context_with_modified_baggage)
                try:
                    async for item in func_instrumented_by_traced(*args, **kwargs):
                        yield item
                finally:
                    otel_context.detach(token)

            return cast(F, baggage_context_wrapper_async_gen)

        elif inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def baggage_context_wrapper_async(*args: Any, **kwargs: Any) -> Any:
                # Ensure Gentrace is initialized (auto-init if possible)
                ensure_initialized(suppress_warnings=suppress_warnings)
                
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
                # Ensure Gentrace is initialized (auto-init if possible)
                ensure_initialized(suppress_warnings=suppress_warnings)
                
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
