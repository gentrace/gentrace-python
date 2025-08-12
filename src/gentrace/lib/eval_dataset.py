import asyncio
import inspect
import logging
from typing import (
    Any,
    Dict,
    List,
    Type,
    Tuple,
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
from typing_extensions import Protocol, TypeAlias, overload, is_typeddict

from pydantic import BaseModel, ValidationError

# Conditional import for TypeAdapter (Pydantic v2 only)
try:
    from pydantic import TypeAdapter

    _HAS_TYPE_ADAPTER = True
except ImportError:
    TypeAdapter = None  # type: ignore
    _HAS_TYPE_ADAPTER = False  # pyright: ignore[reportConstantRedefinition]
from opentelemetry import trace, baggage as otel_baggage, context as otel_context
from opentelemetry.trace.status import Status, StatusCode

from gentrace.types.test_case import TestCase

from .utils import is_ci, is_pydantic_v1, ensure_initialized, _gentrace_json_dumps, display_gentrace_warning
from .progress import ProgressReporter, RichProgressReporter, SimpleProgressReporter
from .warnings import GentraceWarnings
from .constants import (
    ATTR_GENTRACE_SAMPLE_KEY,
    ATTR_GENTRACE_TEST_CASE_ID,
    ATTR_GENTRACE_EXPERIMENT_ID,
    ATTR_GENTRACE_TEST_CASE_NAME,
    MAX_EVAL_DATASET_CONCURRENCY,
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
SchemaType = Union[Type[BaseModel], Any]  # Type for schema (BaseModel or TypedDict)

_tracer = trace.get_tracer("gentrace.sdk")


class TestInputProtocol(Protocol, Generic[InputPayload]):
    id: Optional[str]
    name: Optional[str]
    inputs: InputPayload

    def __getitem__(self, key: str) -> Any: ...


TInputDict = TypeVar("TInputDict", bound=Mapping[str, Any], covariant=True)


class TestInput(BaseModel, Generic[TInputDict]):
    """Local test input as a Pydantic model for evaluation."""

    inputs: TInputDict
    name: Optional[str] = None
    id: Optional[str] = None


DataProviderType: TypeAlias = Union[
    Callable[
        [],
        Union[
            Awaitable[Sequence[Union[TestCase, TestInput[Mapping[str, Any]]]]],
            Sequence[Union[TestCase, TestInput[Mapping[str, Any]]]],
        ],
    ],
    Sequence[Union[TestCase, TestInput[Mapping[str, Any]]]],
]


def _validate_inputs_with_schema(
    inputs: Mapping[str, Any], schema: SchemaType
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Validate inputs using either a Pydantic BaseModel or TypedDict.

    Returns:
        Tuple of (is_valid, validated_data, error_message)
    """
    try:
        # Check if it's a TypedDict
        if is_typeddict(schema):
            if _HAS_TYPE_ADAPTER and TypeAdapter is not None:
                # Use TypeAdapter for Pydantic v2
                adapter = TypeAdapter(schema)
                validated = adapter.validate_python(inputs)
                # TypeAdapter returns the validated data as a dict for TypedDict
                validated_dict = cast(Dict[str, Any], dict(validated) if not isinstance(validated, dict) else validated)
                return True, validated_dict, None
            else:
                # For Pydantic v1, we can't validate TypedDict directly
                # Just return the inputs as-is with a warning
                logger.warning(
                    "TypedDict validation requires Pydantic v2. Inputs will be passed through without validation."
                )
                return True, dict(inputs), None
        else:
            # It's a Pydantic BaseModel
            try:
                if is_pydantic_v1():
                    validated = schema.parse_obj(inputs)  # type: ignore
                else:
                    validated = schema.model_validate(inputs)  # type: ignore

                # Convert to dict for logging
                dict_for_log: Dict[str, Any]
                validated_obj = cast(BaseModel, validated)
                if hasattr(validated_obj, "model_dump"):
                    dict_for_log = validated_obj.model_dump()  # type: ignore
                elif hasattr(validated_obj, "dict"):
                    dict_for_log = validated_obj.dict()  # type: ignore
                else:
                    dict_for_log = dict(validated_obj) if hasattr(validated_obj, "__dict__") else dict(inputs)

                return True, dict_for_log, None
            except AttributeError:
                # Not a BaseModel, just return the inputs
                return True, dict(inputs), None

    except ValidationError as ve:
        return False, None, str(ve)
    except Exception as e:
        # Handle specific Pydantic errors
        error_msg = str(e)
        if "Please use `typing_extensions.TypedDict`" in error_msg:
            return False, None, "TypedDict must be imported from typing_extensions, not typing module"
        return False, None, f"Validation error: {error_msg}"


async def _execute_interaction_function(
    interaction_function: Callable[[TestCase], Union[TResult, Awaitable[TResult]]],
    parsed_input: TestCase,
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
    interaction_function: Callable[[TestCase], Union[TResult, Awaitable[TResult]]],
    input_schema: Optional[SchemaType],
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
        input_schema: Optional Pydantic BaseModel or TypedDict for validation
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
                input_dict_for_log: Any = None

                if input_schema:
                    # Validate the inputs using either Pydantic BaseModel or TypedDict
                    is_valid, validated_data, error_message = _validate_inputs_with_schema(
                        raw_inputs or {},  # Ensure we pass a dict
                        input_schema,
                    )

                    if not is_valid:
                        logger.error(
                            f"Pydantic validation failed for test case {test_case_name}. Inputs: {raw_inputs}. Error: {error_message}"
                        )
                        # Use a generic exception for error recording since we can't create ValidationError directly
                        error = Exception(f"Validation Error: {error_message}")
                        span.record_exception(error)
                        span.set_status(Status(StatusCode.ERROR, description="Input validation failed"))
                        span.set_attribute("error.type", "ValidationError")
                        return None

                    input_dict_for_log = validated_data

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
                    full_test_case,
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


@overload
async def eval_dataset(
    *,
    data: DataProviderType,
    schema: SchemaType,
    interaction: Callable[[TestCase], TResult],
    max_concurrency: Optional[int] = None,
    show_progress_bar: Optional[bool] = None,
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType,
    schema: SchemaType,
    interaction: Callable[[TestCase], Awaitable[TResult]],
    max_concurrency: Optional[int] = None,
    show_progress_bar: Optional[bool] = None,
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType,
    interaction: Callable[[TestCase], TResult],
    max_concurrency: Optional[int] = None,
    show_progress_bar: Optional[bool] = None,
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType,
    interaction: Callable[[TestCase], Awaitable[TResult]],
    max_concurrency: Optional[int] = None,
    show_progress_bar: Optional[bool] = None,
) -> Sequence[Optional[TResult]]: ...


async def eval_dataset(
    *,
    data: DataProviderType,
    schema: Optional[SchemaType] = None,
    interaction: Callable[[Any], Union[TResult, Awaitable[TResult]]],
    max_concurrency: Optional[int] = None,
    show_progress_bar: Optional[bool] = None,
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
        schema (Optional[Union[Type[pydantic.BaseModel], Type[TypedDict]]]): A Pydantic BaseModel or TypedDict
                                                   to validate the `inputs` of each test case. If validation fails
                                                   for a case, an error is logged to its span, and the test case is
                                                   skipped (returning None). TypedDict validation requires Pydantic v2.
        interaction (Callable): The function to test for each test case.
                               Always receives a TestCase object (TestInput is converted
                               internally to TestCase).
        max_concurrency (Optional[int]): Maximum number of test cases to run concurrently.
                                       If None (default), all test cases run concurrently.
                                       Maximum allowed value is 100.
                                       For async functions, uses asyncio.Semaphore.
                                       For sync functions, uses ThreadPoolExecutor.
        show_progress_bar (Optional[bool]): Controls progress display during evaluation.
                                          - True: Shows an interactive progress bar
                                          - False: Shows line-by-line output (for CI/CD)
                                          - None (default): Auto-detects CI environment

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
        if max_concurrency > MAX_EVAL_DATASET_CONCURRENCY:
            warning = GentraceWarnings.HighConcurrencyError(max_concurrency)
            display_gentrace_warning(warning)
            raise ValueError(
                f"max_concurrency ({max_concurrency}) exceeds maximum allowed value of {MAX_EVAL_DATASET_CONCURRENCY}. Please use a value between 1 and {MAX_EVAL_DATASET_CONCURRENCY}."
            )

        semaphore = asyncio.Semaphore(max_concurrency)

    raw_test_cases: Sequence[Union[TestCase, TestInput[Mapping[str, Any]]]]
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
        # Convert TestInput to TestCase internally
        if isinstance(raw_case, TestCase):
            # If already a TestCase, use as-is
            converted_test_cases.append(raw_case)
        else:
            # Generate values for required fields
            now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

            # Convert TestInput to TestCase
            # At this point, raw_case must be TestInput based on the type annotation
            converted_test_cases.append(
                TestCase(
                    id=raw_case.id or "",  # Don't generate ID for local test cases
                    name=raw_case.name or "",  # Let the index-based naming logic handle unnamed cases
                    inputs=dict(raw_case.inputs),  # Convert Mapping to dict
                    expectedOutputs=None,
                    # Fill required fields with sensible defaults
                    datasetId="local",
                    pipelineId="local",
                    createdAt=now,
                    updatedAt=now,
                    archivedAt=None,
                    deletedAt=None,
                )
            )

    # Initialize progress reporter based on configuration
    use_progress_bar = show_progress_bar if show_progress_bar is not None else not is_ci()
    progress_reporter: ProgressReporter
    if use_progress_bar:
        progress_reporter = RichProgressReporter()
    else:
        # Configure logging for SimpleProgressReporter if needed.
        # Unlike normal Stainless behavior (which requires GENTRACE_LOG env var), we set up
        # logging automatically here so progress output works without user configuration.
        parent_logger = logger.parent
        if not logger.handlers and (not parent_logger or not parent_logger.handlers):
            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s",  # Simple format for clean output
                force=False,  # Don't override existing configuration
            )
            logger.setLevel(logging.INFO)
        progress_reporter = SimpleProgressReporter(logger)

    # Start progress reporting with experiment URL if available
    experiment_url = experiment_context.get("experiment_url")
    progress_reporter.start(experiment_context["pipeline_id"], len(converted_test_cases), experiment_url)

    evaluation_tasks: List[Tuple[str, Awaitable[Optional[TResult]]]] = []
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
            # Update progress to show current test
            if hasattr(progress_reporter, "update_current_test"):
                progress_reporter.update_current_test(case_name)

            try:
                result = await _run_single_test_case_for_dataset(
                    test_case_name=case_name,
                    test_case_id=case_id_val,
                    raw_inputs=case_inputs_val,  # type: ignore[arg-type]
                    full_test_case=full_case,
                    interaction_function=interaction_fn,
                    input_schema=input_schema,
                    experiment_context=experiment_context,
                    semaphore=semaphore,
                )
                return result
            finally:
                # Report progress after test completes (success or failure)
                progress_reporter.increment(case_name)

        evaluation_tasks.append((final_case_name, run_test_case()))

    try:
        # Extract just the tasks for gathering
        tasks_only = [task for _, task in evaluation_tasks]
        results = await asyncio.gather(*tasks_only)
    finally:
        # Always stop the progress reporter
        progress_reporter.stop()

    return results


__all__ = ["eval_dataset", "TestInput"]
