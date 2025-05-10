import asyncio
import inspect
from typing import (Any, Awaitable, Callable, Dict, Generic, List, Optional, Type,
                    TypeVar, Union, cast)

from opentelemetry import trace
from opentelemetry.trace.status import StatusCode, Status
from pydantic import BaseModel, ValidationError
from typing_extensions import TypedDict

from .experiment import ExperimentContext, get_current_experiment_context
from .utils import _gentrace_json_dumps, is_pydantic_v1

# Type Variables for eval_dataset
InputPayload = TypeVar("InputPayload")  # Type of the raw inputs within a TestCase
TInput = TypeVar("TInput")           # Type of the (potentially parsed) input to interaction fn
TResult = TypeVar("TResult")         # Return type of the interaction fn

_tracer = trace.get_tracer("gentrace.sdk")

class TestCase(TypedDict, Generic[InputPayload], total=False):
    """Represents a single test case from the dataset."""
    id: Optional[str]
    name: Optional[str]
    inputs: InputPayload 
    expected: Optional[Any] # Expected output, can be of any type
    metadata: Optional[Dict[str, Any]] # Additional metadata for the test case


class EvalDatasetOptions(TypedDict, Generic[TInput, TResult, InputPayload]):
    """Options for configuring an eval_dataset run."""
    interaction: Callable[[Optional[TInput]], Union[TResult, Awaitable[TResult]]]
    data: Callable[[], Union[Awaitable[List[TestCase[InputPayload]]], List[TestCase[InputPayload]]]]
    schema: Optional[Type[BaseModel]] # Pydantic model for validating TestCase.inputs
    dataset_name: Optional[str] # Optional name for the dataset being evaluated


async def _run_single_test_case_for_dataset(
    test_case_name: str,
    test_case_id: Optional[str],
    raw_inputs: Optional[InputPayload],
    expected_output: Optional[Any],
    case_metadata: Optional[Dict[str, Any]],
    interaction_function: Callable[[Optional[TInput]], Union[TResult, Awaitable[TResult]]],
    input_schema: Optional[Type[BaseModel]],
    experiment_context: ExperimentContext,
) -> TResult:
    """
    Internal helper to run and trace a single test case from a dataset.
    This is similar to the logic in the @eval decorator but adapted for dataset items.
    """
    span_name = f"Dataset Eval: {test_case_name}"
    parsed_input_for_interaction: Optional[TInput] = None
    span_event_attributes: Dict[str, str] = {}
    result_value: Any = None # To satisfy linters before assignment in try block

    with _tracer.start_as_current_span(span_name) as span:
        span.set_attribute("gentrace.experiment_id", experiment_context["experiment_id"])
        span.set_attribute("gentrace.pipeline_id", experiment_context["pipeline_id"])
        span.set_attribute("gentrace.test_case.name", test_case_name)
        if test_case_id:
            span.set_attribute("gentrace.test_case.id", test_case_id)
        if expected_output is not None:
             span.set_attribute("gentrace.test_case.expected_output", _gentrace_json_dumps(expected_output))

        if case_metadata:
            for key, value in case_metadata.items():
                attr_key = f"gentrace.metadata.test_case.{key}"
                # Simplified attribute setting from eval.py
                try:
                    span.set_attribute(attr_key, _gentrace_json_dumps(value) if isinstance(value, (dict, list, tuple)) else str(value))
                except Exception:
                    span.set_attribute(attr_key, f"[Unserializable metadata: {key}]")

        try:
            input_dict_for_log: Any = None
            if input_schema:
                model_schema: Type[BaseModel] = input_schema
                if is_pydantic_v1():
                    parsed_input_for_interaction = model_schema.parse_obj(raw_inputs) # type: ignore[assignment]
                else:
                    parsed_input_for_interaction = model_schema.model_validate(raw_inputs) # type: ignore[assignment]
                
                if hasattr(parsed_input_for_interaction, 'model_dump'):
                    input_dict_for_log = parsed_input_for_interaction.model_dump() # type: ignore
                elif hasattr(parsed_input_for_interaction, 'dict'):
                    input_dict_for_log = parsed_input_for_interaction.dict() # type: ignore
                else: 
                    input_dict_for_log = parsed_input_for_interaction
                span_event_attributes["inputs_validated"] = _gentrace_json_dumps(input_dict_for_log)
            elif raw_inputs is not None:
                parsed_input_for_interaction = raw_inputs # type: ignore[assignment]
                input_dict_for_log = raw_inputs
                span_event_attributes["inputs_raw"] = _gentrace_json_dumps(input_dict_for_log)
            else:
                parsed_input_for_interaction = None # type: ignore[assignment]
                input_dict_for_log = None

            if input_dict_for_log is not None or span_event_attributes:
                 span.add_event("eval_dataset.test_case.inputs", span_event_attributes)
            else:
                 span.add_event("eval_dataset.test_case.inputs", {"inputs": "None"})

            if inspect.iscoroutinefunction(interaction_function):
                result_value = await interaction_function(parsed_input_for_interaction)
            else:
                result_value = interaction_function(parsed_input_for_interaction)

            span.add_event("eval_dataset.test_case.outputs", {"outputs": _gentrace_json_dumps(result_value)})
            span.set_status(Status(StatusCode.OK))
            return cast(TResult, result_value)
        except ValidationError as ve:
            span.record_exception(ve)
            span.set_status(Status(StatusCode.ERROR, description="Input validation failed"))
            span.set_attribute("error.type", ve.__class__.__name__)
            # Consider logging SDK error if client available: get_gentrace_client_session().logger.error(...)
            raise # Re-raise for eval_dataset to potentially handle or aggregate
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, description=str(e)))
            span.set_attribute("error.type", e.__class__.__name__)
            raise

async def eval_dataset(
    options: EvalDatasetOptions[TInput, TResult, InputPayload]
) -> List[TResult]:
    """
    Runs a series of test cases from a dataset against a specified interaction function,
    all within an active Gentrace experiment context.

    This function must be called within a function decorated by `@experiment()`.
    Each test case execution is traced as an individual OpenTelemetry span, tagged with
    details from the experiment context and the test case itself.

    Args:
        options: Configuration for the dataset evaluation run:
            interaction (Callable): The function to test for each test case. 
                                   Receives (optionally validated) inputs.
            data (Callable): A function or coroutine function that returns a list of TestCases.
                             Each TestCase should be a dictionary-like object with an `inputs` 
                             key, and optional `id`, `name`, `expected`, and `metadata` keys.
            schema (Optional[Type[pydantic.BaseModel]]): A Pydantic model to validate the `inputs`
                                                       of each TestCase. If validation fails for a
                                                       case, an error is logged to its span, and
                                                       the exception is raised (halting that specific case).
            dataset_name (Optional[str]): An optional name for this dataset evaluation run, primarily for metadata.

    Returns:
        A list containing the results of the `interaction` function for each successfully
        processed test case. If any test case raises an unhandled exception (including
        validation errors), `asyncio.gather` will raise that exception and the 
        overall evaluation will halt.

    Raises:
        RuntimeError: If called outside of an active `@experiment` context or if the 
                      `data` provider fails catastrophically.
        Any exception raised during a specific test case interaction (after validation) 
        will propagate from that specific test case run.
    """
    experiment_context = get_current_experiment_context()
    if not experiment_context:
        raise RuntimeError(
            "eval_dataset must be called within the context of an @experiment() decorated function."
        )

    # Prepare options
    interaction_fn = options["interaction"]
    data_provider = options["data"]
    input_schema = options.get("schema")
    # dataset_name_opt = options.get("dataset_name") # For future metadata use

    raw_test_cases: List[TestCase[InputPayload]]
    try:
        data_result = data_provider()
        if inspect.isawaitable(data_result):
            raw_test_cases = await data_result
        else:
            raw_test_cases = data_result
    except Exception as e:
        # Potentially log this with a Gentrace SDK logger if available
        raise RuntimeError(
            f"Failed to retrieve or process dataset from data provider: {e}"
        ) from e

    evaluation_tasks: List[Awaitable[TResult]] = []
    for i, test_case in enumerate(raw_test_cases):
        case_inputs = test_case.get("inputs")
        case_id = test_case.get("id")
        case_name_prop = test_case.get("name")
        case_expected = test_case.get("expected")
        case_meta = test_case.get("metadata")

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
            raw_inputs=case_inputs, # type: ignore
            expected_output=case_expected,
            case_metadata=case_meta,
            interaction_function=interaction_fn,
            input_schema=input_schema,
            experiment_context=experiment_context,
        )
        evaluation_tasks.append(task)

    results = await asyncio.gather(*evaluation_tasks, return_exceptions=False)
    return results

__all__ = ["eval_dataset", "EvalDatasetOptions", "TestCase"] 