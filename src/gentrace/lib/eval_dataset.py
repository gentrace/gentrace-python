import asyncio
import inspect
import logging
from typing import (
    Any,
    Dict,
    List,
    Type,
    Union,
    Generic,
    Mapping,
    TypeVar,
    Callable,
    Optional,
    Sequence,
    Awaitable,
    cast,
)
from datetime import datetime, timezone
from contextvars import copy_context
from typing_extensions import Protocol, TypeAlias, overload

from pydantic import BaseModel, ValidationError
from opentelemetry import trace, baggage as otel_baggage, context as otel_context
from opentelemetry.trace.status import Status, StatusCode

from gentrace.types.test_case import TestCase

from .utils import is_pydantic_v1, ensure_initialized, _gentrace_json_dumps, display_gentrace_warning
from .warnings import GentraceWarnings
from .constants import (
    ATTR_GENTRACE_SAMPLE_KEY,
    ATTR_GENTRACE_TEST_CASE_ID,
    ATTR_GENTRACE_EXPERIMENT_ID,
    ATTR_GENTRACE_TEST_CASE_NAME,
    ATTR_GENTRACE_FN_ARGS_EVENT_NAME,
    ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME,
)
from .experiment import ExperimentContext, get_current_experiment_context

logger = logging.getLogger("gentrace")

# Type Variables for eval_dataset
InputPayload = TypeVar("InputPayload", bound=Mapping[str, Any])  # Type of the raw inputs within a TestCase
TInput = TypeVar("TInput")  # Type of the (potentially parsed) input to interaction fn
TResult = TypeVar("TResult")  # Return type of the interaction fn
SchemaPydanticModel = TypeVar("SchemaPydanticModel", bound=BaseModel)  # Type for Pydantic schema

_tracer = trace.get_tracer("gentrace.sdk")


class TestInputProtocol(Protocol, Generic[InputPayload]):
    id: Optional[str]
    name: Optional[str]
    inputs: InputPayload

    def __getitem__(self, key: str) -> Any: ...


class TestInput(BaseModel):
    """Local test input as a Pydantic model for evaluation."""
    inputs: Dict[str, Any]
    name: Optional[str] = None
    id: Optional[str] = None


DataProviderType: TypeAlias = Union[
    Callable[
        [],
        Union[
            Awaitable[Sequence[Union[TestCase, TestInput]]],
            Sequence[Union[TestCase, TestInput]],
        ],
    ],
    Sequence[Union[TestCase, TestInput]],
]


async def _execute_interaction_function(
    interaction_function: Callable[[Optional[TInput]], Union[TResult, Awaitable[TResult]]],
    parsed_input: Optional[TInput],
    semaphore: Optional[asyncio.Semaphore],
) -> TResult:
    """
    Execute the interaction function with proper concurrency control.
    Handles both async and sync functions, and applies semaphore if provided.
    """
    async def run_function() -> TResult:
        if inspect.iscoroutinefunction(interaction_function):
            # Async function - just await it
            result = await interaction_function(parsed_input)
            return cast(TResult, result)
        else:
            # Sync function - run in thread pool to avoid blocking
            event_loop = asyncio.get_running_loop()
            ctx = copy_context()
            
            def run_sync() -> Any:
                """Run the sync function with the captured context."""
                return ctx.run(interaction_function, parsed_input)
            
            return await event_loop.run_in_executor(None, run_sync)
    
    # Apply semaphore if provided
    if semaphore:
        async with semaphore:
            return await run_function()
    else:
        return await run_function()


async def _run_single_test_case_for_dataset(
    test_case_name: str,
    test_case_id: Optional[str],
    raw_inputs: Optional[InputPayload],
    full_test_case: TestCase,
    interaction_function: Callable[[Optional[TInput]], Union[TResult, Awaitable[TResult]]],
    input_schema: Optional[Type[BaseModel]],
    experiment_context: ExperimentContext,
    semaphore: Optional[asyncio.Semaphore],
) -> Optional[TResult]:
    """
    Internal helper to run and trace a single test case from a dataset.
    This is similar to the logic in the @eval decorator but adapted for dataset items.
    
    Args:
        test_case_name: Name of the test case for tracing
        test_case_id: Optional ID of the test case
        raw_inputs: The input data for the test case
        interaction_function: The function to test
        input_schema: Optional Pydantic schema for validation
        experiment_context: The experiment context
        semaphore: Optional semaphore for concurrency control
    """
    span_name = test_case_name
    result_value: Any = None  # type: ignore

    # Set up baggage context similar to @interaction()
    current_context = otel_context.get_current()
    context_with_modified_baggage = otel_baggage.set_baggage(ATTR_GENTRACE_SAMPLE_KEY, "true", context=current_context)

    token = otel_context.attach(context_with_modified_baggage)
    try:
        with _tracer.start_as_current_span(span_name) as span:
            span.set_attribute(ATTR_GENTRACE_EXPERIMENT_ID, experiment_context["experiment_id"])
            span.set_attribute(ATTR_GENTRACE_TEST_CASE_NAME, test_case_name)
            if test_case_id:
                span.set_attribute(ATTR_GENTRACE_TEST_CASE_ID, test_case_id)

            try:
                # Prepare the test case to pass to interaction function
                test_case_for_interaction: Optional[TInput] = full_test_case  # type: ignore
                input_dict_for_log: Any = None

                if input_schema:
                    # Validate the inputs against Pydantic schema
                    model_schema = input_schema
                    try:
                        if is_pydantic_v1():
                            validated = model_schema.parse_obj(raw_inputs)  # type: ignore
                        else:
                            validated = model_schema.model_validate(raw_inputs)

                        # Log the dictified validated model
                        if hasattr(validated, "model_dump"):
                            input_dict_for_log = validated.model_dump()
                        elif hasattr(validated, "dict"):
                            input_dict_for_log = validated.dict()  # type: ignore
                        else:
                            input_dict_for_log = validated
                        
                        # Keep the TestCase object but update its inputs with validated data
                        # This ensures the interaction function always receives a TestCase
                        test_case_for_interaction = full_test_case  # type: ignore
                            
                    except ValidationError as ve:
                        logger.error(
                            f"Pydantic validation failed for test case {test_case_name}. Inputs: {raw_inputs}",
                            exc_info=True,
                        )
                        span.record_exception(ve)
                        span.set_status(Status(StatusCode.ERROR, description="Input validation failed"))
                        span.set_attribute("error.type", ve.__class__.__name__)
                        return None

                elif raw_inputs is not None:
                    # No schema → just log the raw dict
                    input_dict_for_log = raw_inputs
                else:
                    # both schema is None and raw_inputs is None
                    input_dict_for_log = None

                # Attach the inputs as a span event
                if input_dict_for_log is not None:
                    span.add_event(
                        ATTR_GENTRACE_FN_ARGS_EVENT_NAME,
                        {"args": _gentrace_json_dumps([input_dict_for_log])},
                    )

                # Call the interaction function with proper concurrency control
                result_value = await _execute_interaction_function(
                    interaction_function,
                    test_case_for_interaction,
                    semaphore,
                )

                # Log the output
                span.add_event(ATTR_GENTRACE_FN_OUTPUT_EVENT_NAME, {"output": _gentrace_json_dumps(result_value)})
                return cast(Optional[TResult], result_value)

            except Exception as e:
                logger.error(
                    f"Unknown error occurred while running test case {test_case_name}",
                    exc_info=True,
                )
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, description=str(e)))
                span.set_attribute("error.type", e.__class__.__name__)
                return None
    finally:
        otel_context.detach(token)


def _convert_to_test_case(
    item: Union[TestCase, TestInput], 
    pipeline_id: Optional[str] = None
) -> TestCase:
    """Convert TestInput to TestCase internally."""
    
    # If already a TestCase, return as-is
    if isinstance(item, TestCase):
        return item
    
    # Generate values for required fields
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Convert TestInput to TestCase
    # At this point, item must be TestInput based on the type annotation
    return TestCase(
        id=item.id or "",  # Don't generate ID for local test cases
        name=item.name or "Unnamed Test",
        inputs=item.inputs,
        expectedOutputs=None,
        # Fill required fields with sensible defaults
        datasetId="local",
        pipelineId=pipeline_id or "local",
        createdAt=now,
        updatedAt=now,
        archivedAt=None,
        deletedAt=None
    )


@overload
async def eval_dataset(
    *,
    data: DataProviderType,
    schema: Type[SchemaPydanticModel],
    interaction: Callable[[TestCase], TResult],
    max_concurrency: Optional[int] = None,
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType,
    schema: Type[SchemaPydanticModel],
    interaction: Callable[[TestCase], Awaitable[TResult]],
    max_concurrency: Optional[int] = None,
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType,
    interaction: Callable[[TestCase], TResult],
    max_concurrency: Optional[int] = None,
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType,
    interaction: Callable[[TestCase], Awaitable[TResult]],
    max_concurrency: Optional[int] = None,
) -> Sequence[Optional[TResult]]: ...


async def eval_dataset(
    *,
    data: DataProviderType,
    schema: Optional[Type[SchemaPydanticModel]] = None,
    interaction: Callable[[Any], Union[TResult, Awaitable[TResult]]],
    max_concurrency: Optional[int] = None,
) -> Sequence[Optional[TResult]]:
    """
    Runs a series of test cases from a dataset against a specified interaction function,
    all within an active Gentrace experiment context.

    This function must be called within a function decorated by `@experiment()`.
    Each test case execution is traced as an individual OpenTelemetry span, tagged with
    details from the experiment context and the test case itself.

    Args:
        data (Union[Callable, Sequence]): Either a function/coroutine function that returns a list 
                         of test cases, or a plain list of test cases directly.
                         Test cases can be TestCase objects (from API) or TestInput objects (for local tests).
        schema (Optional[Type[pydantic.BaseModel]]): A Pydantic model to validate the `inputs`
                                                   of each TestInput. If validation fails for a
                                                   case, an error is logged to its span, and the
                                                   test case is skipped (returning None).
        interaction (Callable): The function to test for each test case.
                               Always receives a TestCase object (TestInput is converted 
                               internally to TestCase).
        max_concurrency (Optional[int]): Maximum number of test cases to run concurrently.
                                       If None (default), all test cases run concurrently.
                                       For async functions, uses asyncio.Semaphore.
                                       For sync functions, uses ThreadPoolExecutor.

    Returns:
        A list containing the results of the `interaction` function for each successfully
        processed test case. Failed test cases (e.g. due to input validation errors)
        will have a corresponding `None` value in the list.

    Raises:
        RuntimeError: If called outside of an active `@experiment` context or if the
                      `data` provider fails catastrophically.
        Any exception raised during a specific test case interaction (after validation)
        will propagate from that specific test case run.
    """
    ensure_initialized()
    experiment_context = get_current_experiment_context()
    if not experiment_context:
        raise RuntimeError("eval_dataset must be called within the context of an @experiment() decorated function.")

    interaction_fn = interaction
    data_provider = data
    input_schema = schema

    # Create a semaphore for concurrency control if max_concurrency is specified
    semaphore: Optional[asyncio.Semaphore] = None
    if max_concurrency is not None and max_concurrency > 0:
        # Throw exception if max_concurrency is very high
        if max_concurrency > 30:
            warning = GentraceWarnings.HighConcurrencyError(max_concurrency)
            display_gentrace_warning(warning)
            raise ValueError(f"max_concurrency ({max_concurrency}) exceeds maximum allowed value of 30. Please use a value between 1 and 30.")
        
        semaphore = asyncio.Semaphore(max_concurrency)

    raw_test_cases: Sequence[Union[TestCase, TestInput]]
    try:
        if callable(data_provider):
            data_result = data_provider()
            if inspect.isawaitable(data_result):
                raw_test_cases = await data_result
            else:
                raw_test_cases = data_result
        else:
            # data_provider is already a sequence
            raw_test_cases = data_provider
    except Exception as e:
        # Potentially log this with a Gentrace SDK logger if available
        raise RuntimeError(f"Failed to retrieve or process dataset from data provider: {e}") from e

    # Convert all test cases to TestCase objects
    converted_test_cases: List[TestCase] = []
    for raw_case in raw_test_cases:
        # Try to get pipeline_id from experiment context if available
        pipeline_id = getattr(experiment_context, 'pipeline_id', None) if experiment_context else None
        converted_test_cases.append(_convert_to_test_case(raw_case, pipeline_id))

    evaluation_tasks: List[Awaitable[Optional[TResult]]] = []
    for i, test_case in enumerate(converted_test_cases):
        # Now test_case is always a TestCase object
        case_inputs = test_case.inputs
        case_id = test_case.id
        case_name_prop = test_case.name

        final_case_name: str
        if case_name_prop:
            final_case_name = case_name_prop
        elif case_id:
            final_case_name = f"Test Case (ID: {case_id})"
        else:
            final_case_name = f"Test Case {i + 1}"

        # Create the task - semaphore will be handled inside _run_single_test_case_for_dataset
        async def run_test_case(
            case_name: str = final_case_name,
            case_id_val: Optional[str] = case_id,
            case_inputs_val: Mapping[str, Any] = case_inputs,
            full_case: TestCase = test_case,
        ) -> Optional[TResult]:
            return await _run_single_test_case_for_dataset(
                test_case_name=case_name,
                test_case_id=case_id_val,
                raw_inputs=case_inputs_val,  # type: ignore[arg-type]
                full_test_case=full_case,
                interaction_function=interaction_fn,
                input_schema=input_schema,
                experiment_context=experiment_context,
                semaphore=semaphore,
            )
        
        evaluation_tasks.append(run_test_case())

    results = await asyncio.gather(*evaluation_tasks)
    return results


__all__ = ["eval_dataset", "TestInput"]
