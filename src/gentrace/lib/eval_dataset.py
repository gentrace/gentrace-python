import asyncio
import inspect
import logging
from typing import (
    Any,
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
from typing_extensions import Protocol, TypeAlias, TypedDict, overload

from pydantic import BaseModel, ValidationError
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

from gentrace.types.test_case import TestCase

from .utils import is_pydantic_v1, _gentrace_json_dumps, check_otel_config_and_warn
from .constants import (
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


class TestInput(TypedDict, Generic[InputPayload], total=False):
    name: str
    inputs: InputPayload


DataProviderType: TypeAlias = Callable[
    [],
    Union[
        Awaitable[Sequence[Union[TestCase, TestInput[InputPayload]]]],
        Sequence[Union[TestCase, TestInput[InputPayload]]],
    ],
]


async def _run_single_test_case_for_dataset(
    test_case_name: str,
    test_case_id: Optional[str],
    raw_inputs: Optional[InputPayload],
    interaction_function: Callable[[Optional[TInput]], Union[TResult, Awaitable[TResult]]],
    input_schema: Optional[Type[BaseModel]],
    experiment_context: ExperimentContext,
) -> Optional[TResult]:
    """
    Internal helper to run and trace a single test case from a dataset.
    This is similar to the logic in the @eval decorator but adapted for dataset items.
    """
    span_name = test_case_name
    result_value: Any = None  # type: ignore

    with _tracer.start_as_current_span(span_name) as span:
        span.set_attribute(ATTR_GENTRACE_EXPERIMENT_ID, experiment_context["experiment_id"])
        span.set_attribute(ATTR_GENTRACE_TEST_CASE_NAME, test_case_name)
        if test_case_id:
            span.set_attribute(ATTR_GENTRACE_TEST_CASE_ID, test_case_id)

        try:
            # Always pass the raw dict (or None) into the interaction fn
            parsed_input_for_interaction: Optional[TInput] = raw_inputs  # type: ignore
            input_dict_for_log: Any = None

            if input_schema:
                # Validate against Pydantic but do *not* pass the model instance downstream
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

            # Call the interaction function with the original dict (or None)
            if inspect.iscoroutinefunction(interaction_function):
                result_value = await interaction_function(parsed_input_for_interaction)
            else:
                result_value = interaction_function(parsed_input_for_interaction)

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


@overload
async def eval_dataset(
    *,
    data: DataProviderType[InputPayload],
    schema: Type[SchemaPydanticModel],
    interaction: Callable[[InputPayload], TResult],
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType[InputPayload],
    schema: Type[SchemaPydanticModel],
    interaction: Callable[[InputPayload], Awaitable[TResult]],
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType[InputPayload],
    interaction: Callable[[InputPayload], TResult],
) -> Sequence[Optional[TResult]]: ...


@overload
async def eval_dataset(
    *,
    data: DataProviderType[InputPayload],
    interaction: Callable[[InputPayload], Awaitable[TResult]],
) -> Sequence[Optional[TResult]]: ...


async def eval_dataset(
    *,
    data: DataProviderType[InputPayload],
    schema: Optional[Type[SchemaPydanticModel]] = None,
    interaction: Callable[[Any], Union[TResult, Awaitable[TResult]]],
) -> Sequence[Optional[TResult]]:
    """
    Runs a series of test cases from a dataset against a specified interaction function,
    all within an active Gentrace experiment context.

    This function must be called within a function decorated by `@experiment()`.
    Each test case execution is traced as an individual OpenTelemetry span, tagged with
    details from the experiment context and the test case itself.

    Args:
        data (Callable): A function or coroutine function that returns a list of TestInputs.
                         Each TestInput should be a dictionary-like object with an `inputs`
                         key, and optional `id`, `name` keys. Can be either TestInputProtocol
                         or TestInput[InputPayload].
        schema (Optional[Type[pydantic.BaseModel]]): A Pydantic model to validate the `inputs`
                                                   of each TestInput. If validation fails for a
                                                   case, an error is logged to its span, and
                                                   the exception is raised (halting that specific case).
        interaction (Callable): The function to test for each test case.
                               Receives (optionally validated) inputs.

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
    check_otel_config_and_warn()
    experiment_context = get_current_experiment_context()
    if not experiment_context:
        raise RuntimeError("eval_dataset must be called within the context of an @experiment() decorated function.")

    interaction_fn = interaction
    data_provider = data
    input_schema = schema

    raw_test_cases: Sequence[Union[TestCase, TestInput[InputPayload]]]
    try:
        data_result = data_provider()
        if inspect.isawaitable(data_result):
            raw_test_cases = await data_result
        else:
            raw_test_cases = data_result
    except Exception as e:
        # Potentially log this with a Gentrace SDK logger if available
        raise RuntimeError(f"Failed to retrieve or process dataset from data provider: {e}") from e

    evaluation_tasks: List[Awaitable[Optional[TResult]]] = []
    for i, test_case in enumerate(raw_test_cases):
        case_inputs: Optional[InputPayload]
        case_id: Optional[str]
        case_name_prop: Optional[str]

        if isinstance(test_case, dict):
            # TypedDict case
            case_inputs = test_case.get("inputs")
            case_id = None
            case_name_prop = test_case.get("name")
        else:
            protocol_case = test_case
            case_inputs = cast(InputPayload, protocol_case.inputs)
            case_id = protocol_case.id
            case_name_prop = protocol_case.name

        final_case_name: str
        if case_name_prop:
            final_case_name = case_name_prop
        elif case_id:
            final_case_name = f"Test Case (ID: {case_id})"
        else:
            final_case_name = f"Test Case {i + 1}"

        task = _run_single_test_case_for_dataset(
            test_case_name=final_case_name,
            test_case_id=case_id,
            raw_inputs=case_inputs,
            interaction_function=interaction_fn,
            input_schema=input_schema,
            experiment_context=experiment_context,
        )
        evaluation_tasks.append(task)

    results = await asyncio.gather(*evaluation_tasks)
    return results


__all__ = ["eval_dataset", "TestInput"]
