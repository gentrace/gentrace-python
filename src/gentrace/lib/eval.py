import functools
import inspect
from typing import Any, Callable, Coroutine, Dict, Optional, TypeVar, overload

from opentelemetry import trace
from opentelemetry.trace.status import StatusCode, Status
from typing_extensions import ParamSpec

from .constants import ANONYMOUS_SPAN_NAME
from .experiment import ExperimentContext, get_current_experiment_context
from .utils import _gentrace_json_dumps # For safe serialization of output

P = ParamSpec("P")
R = TypeVar("R")

_tracer = trace.get_tracer("gentrace.sdk")

@overload
def eval(
    name: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
    ...

@overload
def eval(
    name: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable[[Callable[P, R]], Callable[P, Coroutine[Any, Any, R]]]: # Sync func becomes awaitable
    ...

def eval(
    name: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable[[Callable[P, Any]], Callable[P, Coroutine[Any, Any, Any]]]:
    """
    Decorator factory to mark a function as a single evaluation test case within an experiment.

    This decorator must be used on a function that is called within the scope of an
    `@experiment()` decorated function.

    When the decorated function is called:
    1. It retrieves the current `experiment_id` and `pipeline_id` from the context
       set by `@experiment()`.
    2. It creates an OpenTelemetry span representing this specific evaluation.
       The span is named using the provided `name` argument.
    3. Attributes `gentrace.experiment_id`, `gentrace.pipeline_id`, and 
       `gentrace.eval.name` are set on the span.
    4. Any provided `metadata` is added to the span, prefixed with `gentrace.metadata.eval.`.
    5. The decorated function's execution (inputs, output, errors) is captured within this span.
    6. If the decorated function is synchronous, it is wrapped to be awaitable, fitting into
       the common asynchronous flow of experiment execution.

    Args:
        name: A descriptive name for this evaluation test case. This will be used as part
              of the OTEL span name and as an attribute.
        metadata: Optional dictionary of arbitrary metadata to attach to this evaluation's span.

    Returns:
        A decorator that wraps the user's function.
    """
    def inner_decorator(func: Callable[P, Any]) -> Callable[P, Coroutine[Any, Any, Any]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            experiment_context: Optional[ExperimentContext] = get_current_experiment_context()

            if not experiment_context:
                func_name = getattr(func, '__name__', ANONYMOUS_SPAN_NAME)
                raise RuntimeError(
                    f"@eval(name='{name}') on function '{func_name}' must be called within an active @experiment context."
                )

            span_name = f"Eval: {name}"
            
            with _tracer.start_as_current_span(span_name) as span:
                span.set_attribute("gentrace.experiment_id", experiment_context["experiment_id"])
                span.set_attribute("gentrace.pipeline_id", experiment_context["pipeline_id"])
                span.set_attribute("gentrace.eval.name", name)

                if metadata:
                    for key, value in metadata.items():
                        attr_key = f"gentrace.metadata.eval.{key}"
                        try:
                            if isinstance(value, (dict, list, tuple)):
                                span.set_attribute(attr_key, _gentrace_json_dumps(value))
                            elif value is not None:
                                span.set_attribute(attr_key, str(value))
                        except Exception:
                            span.set_attribute(attr_key, f"[Unserializable metadata: {key}]")
                
                # Capture inputs if any (though for this simple eval, args/kwargs might be empty)
                # For more complex scenarios, eval_function might take specific inputs.
                # Here, we log what was passed to the decorated function.
                if args or kwargs:
                    input_payload: Dict[str, Any] = {}
                    if args:
                        input_payload["args"] = args
                    if kwargs:
                        input_payload["kwargs"] = kwargs
                    span.add_event("eval.inputs", {"inputs": _gentrace_json_dumps(input_payload)})

                try:
                    if inspect.iscoroutinefunction(func):
                        result = await func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    
                    span.add_event("eval.outputs", {"outputs": _gentrace_json_dumps(result)})
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, description=str(e)))
                    span.set_attribute("error.type", e.__class__.__name__)
                    raise
        return wrapper
    return inner_decorator

__all__ = ["eval"] 