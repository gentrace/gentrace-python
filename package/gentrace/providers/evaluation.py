import copy
import json
import os
import uuid
from itertools import zip_longest
from typing import Any, Callable, Dict, List, Optional, TypedDict, Union

from gentrace.api_client import ApiClient
from gentrace.apis.tags.v1_api import V1Api
from gentrace.apis.tags.v2_api import V2Api
from gentrace.model.expanded_test_result import ExpandedTestResult
from gentrace.model.pipeline import Pipeline
from gentrace.model.test_case import TestCase
from gentrace.model.test_case_v2 import TestCaseV2
from gentrace.models import CreateMultipleTestCases, TestResult
from gentrace.providers.context import ResultContext
from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)
from gentrace.providers.pipeline_run import flush
from gentrace.providers.utils import (
    decrement_test_counter,
    get_test_counter,
    increment_test_counter,
)


class Result(TypedDict):
    resultId: str


class TestCaseDict(TypedDict):
    id: str
    createdAt: str
    updatedAt: str
    archivedAt: Optional[str]
    expectedOutputs: Optional[Dict[str, Any]]
    inputs: Dict[str, Any]
    name: str
    pipelineId: str


def is_valid_uuid(val: str):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def get_test_cases(
        pipeline_id: Optional[str] = None,
        pipeline_slug: Optional[str] = None,
) -> List[TestCase]:
    """
    Retrieves test cases for a given pipeline ID from the Gentrace API.

    Args:
        pipeline_slug (str): The pipeline slug to retrieve test cases for.
        pipeline_id (str): DEPRECATED: The ID of the pipeline to retrieve test cases for.

    Raises:
        ValueError: If the SDK is not initialized. Call init() first.

    Returns:
        list: A list of test cases.
    """

    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    if not pipeline_id and not pipeline_slug:
        raise ValueError("pipeline_slug must be passed")

    effective_pipeline_id = pipeline_id

    if pipeline_slug and not is_valid_uuid(pipeline_slug):
        all_pipelines = get_pipelines(slug=pipeline_slug)

        matching_pipeline = next(
            (
                pipeline
                for pipeline in all_pipelines
                if pipeline["slug"] == pipeline_slug
            ),
            None,
        )

        if not matching_pipeline:
            raise ValueError(f"Could not find the specified pipeline ({pipeline_slug})")

        effective_pipeline_id = matching_pipeline.get("id")

    response = api.v1_test_case_get({"pipelineId": effective_pipeline_id})
    test_cases = response.body.get("testCases", [])
    return test_cases


def get_test_case(
        case_id: str,
) -> TestCaseV2:
    """
    Retrieves a test case for a given test case ID from the Gentrace API.

    Args:
        case_id (str): The test case ID to retrieve.

    Raises:
        ValueError: If the SDK is not initialized. Call init() first.

    Returns:
        TestCaseV2: The test case.
    """

    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V2Api(api_client=api_client)

    response = api.v2_test_cases_id_get({"id": case_id})
    test_case = response.body
    return test_case


class CreateTestCasePayload(TypedDict):
    name: str
    inputs: Dict[str, Any]
    expectedOutputs: Optional[Dict[str, Any]]


class SingleTestCasePayload(TypedDict):
    name: str
    inputs: Dict[str, Any]
    expectedOutputs: Optional[Dict[str, Any]]


class UpdateTestCasePayload(TypedDict):
    id: str
    name: Optional[str]
    inputs: Optional[Dict[str, Any]]
    expectedOutputs: Optional[Dict[str, Any]]
    archived: Optional[bool]


class UpdateTestCaseResponse(TypedDict):
    caseId: str


def create_test_cases(
        pipeline_slug: str,
        payload: List[TestCaseDict],
) -> int:
    """Creates multiple test cases for a specified pipeline using the Gentrace API.

    Parameters:
    - pipeline_slug (str): The unique identifier of the pipeline to which the test cases should be added.
    - payload (List[TestCaseDict]): The array payload containing the test cases to be created.

    Returns:
    - int: Count of test cases created.

    Raises:
    - ValueError: If the Gentrace API key is not initialized or if the pipeline_slug is not passed.

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    if not pipeline_slug:
        raise ValueError("pipeline_slug must be passed")

    response = api.v1_test_case_post({"pipelineSlug": pipeline_slug, "testCases": payload})
    count = response.body.get("creationCount", None)
    return count


def create_test_case(
        pipeline_slug: str,
        payload: SingleTestCasePayload,
) -> str:
    """
    Creates a single test case for a specified pipeline using the Gentrace API.

    Parameters:
    - pipeline_slug (str): The unique identifier of the pipeline to which the test case should be added.
    - payload (SingleTestCasePayload): The payload containing the test case to be created.

    Returns:
    - str: The identifier (caseId) of the created test case.

    Raises:
    - ValueError: If the Gentrace API key is not initialized or if the pipeline_slug is not passed.

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    if not pipeline_slug:
        raise ValueError("pipeline_slug must be passed")

    response = api.v1_test_case_post({"pipelineSlug": pipeline_slug, **payload})
    case_id = response.body.get("caseId", None)
    return case_id


def update_test_case(pipeline_slug: str, payload: UpdateTestCasePayload) -> str:
    """
    Updates a test case for a specified pipeline using the Gentrace API.

    Parameters:
    - pipeline_slug (str): The unique identifier of the pipeline where the test case exists.
    - payload (UpdateTestCasePayload): The payload containing details of the test case to be updated.

    Returns:
    - str: The identifier (caseId) of the updated test case.

    Raises:
    - ValueError: If the Gentrace API key is not initialized or if the pipeline_slug is not passed.

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    if not pipeline_slug:
        raise ValueError("pipeline_slug must be passed")

    response = api.v1_test_case_patch({"pipelineSlug": pipeline_slug, **payload})
    case_id = response.body.get("caseId", None)
    return case_id


def submit_prepared_test_runs(pipeline_slug: str, test_runs: List[Dict],
                              context: Optional[ResultContext] = None) -> Result:
    """
    INTERNAL TO PACKAGE:

    Submits prepared test runs to the Gentrace API for a given pipeline ID. This method requires that you
    create TestRun objects yourself. We recommend using the submit_test_result method instead.

    Args:
        pipeline_slug (str): The pipeline slug
        test_runs (List[Dict]): A list of test runs to submit.

    Raises:
        ValueError: If the SDK is not initialized. Call init() first.

    Returns:
        Run: The response data from the API.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    for test_run in test_runs:
        test_run["inputs"] = (
            json.dumps(test_run["inputs"])
            if isinstance(test_run["inputs"], str)
            else test_run["inputs"]
        )

    params = construct_submission_payload(pipeline_slug, test_runs, context)
    response = api.v1_test_result_simple_post(params)
    return response.body


def construct_submission_payload(pipeline_slug: str, test_runs: List[Dict], context: Optional[ResultContext] = None):
    """
    Constructs a dictionary payload for submitting test runs to a server.

    Args:
        pipeline_slug (str): The pipeline slug
        test_results (List[Dict]): A list of dictionaries containing test results.
        context (Optional[ResultContext]): Context key pairs

    Returns:
        Dict: A dictionary payload containing the pipeline slug, test runs, and optional branch and commit information.
    """
    params = {
        "pipelineSlug": pipeline_slug,
        "testRuns": test_runs,
    }

    if GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"]:
        params["name"] = GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"]

    if GENTRACE_CONFIG_STATE["GENTRACE_RESULT_NAME"]:
        params["name"] = GENTRACE_CONFIG_STATE["GENTRACE_RESULT_NAME"]

    if os.getenv("GENTRACE_BRANCH") or GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"]:
        params["branch"] = GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"] or os.getenv(
            "GENTRACE_BRANCH"
        )

    if os.getenv("GENTRACE_COMMIT") or GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"]:
        params["commit"] = GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"] or os.getenv(
            "GENTRACE_COMMIT"
        )

    if context and context.get("metadata"):
        params["metadata"] = context.get("metadata")

    return params


class OutputStep(TypedDict):
    key: str
    output: str
    inputs: Optional[Dict[str, Any]]


def submit_test_result(
        pipeline_slug: str,
        test_cases: List[TestCase],
        outputs_list: List[Dict[str, Any]],
        context: Optional[ResultContext] = None
) -> Result:
    """
    Submits a test result by creating TestRun objects from given test cases and corresponding outputs.
    To use a Gentrace runner to capture intermediate steps, use run_test instead.

    Args:
        pipeline_slug (str): The pipeline slug
        test_cases (List[TestCase]): A list of TestCase objects.
        outputs_list (List[Dict[str, Any]]): A list of outputs corresponding to each TestCase.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        Run: The response data from the test_result_simple_post SDK method.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    if len(test_cases) != len(outputs_list):
        raise ValueError("`test_cases` and `outputs` should be the same length.")

    if is_valid_uuid(pipeline_slug):
        raise ValueError("You passed a pipeline ID instead of a pipeline slug.")

    test_runs = []

    for test_case, outputs in zip_longest(test_cases, outputs_list, fillvalue=None):
        result = {
            "caseId": test_case["id"],
            "inputs": json.loads(test_case["inputs"])
            if isinstance(test_case["inputs"], str)
            else test_case["inputs"],
            "outputs": outputs,
        }

        test_runs.append(result)

    return submit_prepared_test_runs(pipeline_slug, test_runs, context)


def get_pipelines(
        label: Optional[str] = None,
        slug: Optional[str] = None,
) -> List[Pipeline]:
    """
    Get pipelines from the Gentrace API, optionally filtered by label or by slug

    Args:
        label (str, optional): The label of the test set. Defaults to None.
        slug (str, optional): The slug of the test set. Defaults to None.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        Run: The array of test sets returned by the Gentrace API.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    params = {}

    if label:
        params["label"] = label

    if slug:
        params["slug"] = slug

    response = api.v1_pipelines_get(params)

    pipelines = response.body.get("pipelines")

    return pipelines


def get_test_result(result_id: str) -> ExpandedTestResult:
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    params = {}

    if result_id:
        params["id"] = result_id

    response = api.v1_test_result_id_get(params)

    return response.body


def get_test_results(
        pipeline_slug: str,
) -> List[TestResult]:
    """
    Fetches test results using the Gentrace API.

    Args:
        pipeline_slug (str): The pipeline slug to pull test results

    Returns:
        List[TestResult]: A list of test results fetched from the Gentrace API.

    Raises:
        ValueError: If the Gentrace API key is not initialized. Call `init()` function first.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    params = {}

    if pipeline_slug:
        params["pipelineSlug"] = pipeline_slug

    response = api.v1_test_result_get(params)

    test_results = response.body.get("testResults")

    return test_results


class EvaluationDictBase(TypedDict, total=True):
    evaluatorId: str
    runId: str
    note: Optional[str]


class EvaluationDict(EvaluationDictBase, total=False):
    evalValue: Optional[float]
    evalLabel: Optional[str]


def bulk_create_evaluations(
        payloads: List[EvaluationDict],
):
    """
    Creates multiple evaluations using the Gentrace API.

    Args:
        payloads (List[EvaluationDict]): The array payload containing the evaluations to be created.

    Returns:
        int: Count of evaluations created.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V2Api(api_client=api_client)

    result = api.v2_evaluations_bulk_post({
        "data": payloads
    })

    count = result.body.get("count", None)
    return count


def run_test(pipeline_slug: str, handler, context: Optional[ResultContext] = None,
             case_filter: Optional[Callable[[TestCase], bool]] = None) -> Result:
    """
    Runs a test by pulling down test cases from Gentrace, running them through †he
    provided callback (once per test case), and submitting the result report back to Gentrace.

    Args:
        pipeline_slug (str): The slug of the pipeline to run.
        handler (Callable[[TestCase], List[Dict]]): A function that takes a TestCase and returns a tuple of
          the output and a PipelineRun class instance that contains the list of steps taken by the pipeline.
        context (Optional[ResultContext]): Context key pairs
        case_filter: Optional[Callable[[TestCase], bool]] = None

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        Response data from the Gentrace API's /test-result POST method. This should just be a dictionary
        similar to the following:

        {
            "resultId": "161c623d-ee92-417f-823a-cf9f7eccf557",
        }
    """
    increment_test_counter()

    try:
        config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
        if not config:
            raise ValueError("Gentrace API key not initialized. Call init() first.")

        api_client = ApiClient(configuration=config)
        api = V1Api(api_client=api_client)

        all_pipelines = get_pipelines()

        matching_pipeline = next(
            (
                pipeline
                for pipeline in all_pipelines
                if pipeline["slug"] == pipeline_slug
            ),
            None,
        )

        if not matching_pipeline:
            raise ValueError(f"Could not find the specified pipeline ({pipeline_slug})")

        test_cases = get_test_cases(matching_pipeline["id"])

        test_runs = []

        for test_case in test_cases:
            if case_filter and not case_filter(test_case):
                continue

            [output, pipeline_run] = handler(test_case)

            merged_metadata = {}

            step_runs_data = []
            for step_run in pipeline_run.step_runs:
                # Extract metadata without mutating original contexts
                this_context = copy.deepcopy(pipeline_run.context)
                this_context_metadata = this_context.get("metadata", {})
                step_run_context = copy.deepcopy(step_run.context)
                step_run_context_metadata = step_run_context.get("metadata", {})

                merged_metadata.update(this_context_metadata)
                merged_metadata.update(step_run_context_metadata)

                this_context.pop("metadata", None)
                step_run_context.pop("metadata", None)

                this_context.pop("previousRunId", None)
                step_run_context.pop("previousRunId", None)

                step_runs_data.append(
                    {
                        "providerName": step_run.provider,
                        "invocation": step_run.invocation,
                        "modelParams": step_run.model_params,
                        "inputs": step_run.inputs,
                        "outputs": step_run.outputs,
                        "elapsedTime": step_run.elapsed_time,
                        "startTime": step_run.start_time,
                        "endTime": step_run.end_time,
                        "context": {**this_context, **step_run_context},
                    }
                )

            test_run = {
                "caseId": test_case["id"],
                "metadata": merged_metadata,
                "previousRunId": pipeline_run.context.get("previousRunId"),
                "stepRuns": step_runs_data,
            }

            if pipeline_run.get_id():
                test_run["id"] = pipeline_run.get_id()

            test_runs.append(test_run)

        params = {
            "pipelineId": matching_pipeline["id"],
            "testRuns": test_runs,
        }

        if GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"]:
            params["name"] = GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"]

        if GENTRACE_CONFIG_STATE["GENTRACE_RESULT_NAME"]:
            params["name"] = GENTRACE_CONFIG_STATE["GENTRACE_RESULT_NAME"]

        if os.getenv("GENTRACE_BRANCH") or GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"]:
            params["branch"] = GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"] or os.getenv(
                "GENTRACE_BRANCH"
            )

        if os.getenv("GENTRACE_COMMIT") or GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"]:
            params["commit"] = GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"] or os.getenv(
                "GENTRACE_COMMIT"
            )

        if context and context.get("metadata"):
            params["metadata"] = context.get("metadata")

        params["collectionMethod"] = "runner"

        response = api.v1_test_result_post(params)
        return response.body
    except Exception as e:
        raise e
    finally:
        decrement_test_counter()

        # OK to flush here and introduce more latency since this is just used for test anyway
        flush()


__all__ = [
    "get_test_cases",
    "get_test_case",
    "create_test_cases",
    "create_test_case",
    "get_test_results",
    "get_test_result",
    "update_test_case",
    "submit_test_result",
    "get_pipelines",
    "construct_submission_payload",
    "run_test",
    "bulk_create_evaluations",
    "OutputStep",
    "EvaluationDict"
]
