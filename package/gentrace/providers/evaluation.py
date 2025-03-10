import copy
import json
import os
import uuid
from datetime import datetime
from itertools import zip_longest
from typing import Any, Callable, Dict, List, Optional, Tuple, TypedDict

from gentrace.api_client import ApiClient
from gentrace.apis.tags.v1_api import V1Api
from gentrace.apis.tags.v2_api import V2Api
from gentrace.model.evaluator_v2 import EvaluatorV2
from gentrace.model.expanded_test_result import ExpandedTestResult
from gentrace.model.pipeline import Pipeline
from gentrace.model.test_case import TestCase
from gentrace.model.test_case_v2 import TestCaseV2
from gentrace.models import TestResult
from gentrace.providers.context import ResultContext
from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)
from gentrace.providers.pipeline_run import PipelineRun, flush
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


def get_evaluators(
        pipeline_id: Optional[str] = None,
        pipeline_slug: Optional[str] = None,
) -> List[EvaluatorV2]:
    """
    Retrieves evaluators  for a given pipeline ID from the Gentrace API.

    Args:
        pipeline_slug (str): The pipeline slug to retrieve evaluators for.
        pipeline_id (str): The ID of the pipeline to retrieve evaluators for.

    Raises:
        ValueError: If the SDK is not initialized. Call init() first.

    Returns:
        list: A list of evaluators.
    """

    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V2Api(api_client=api_client)

    if not pipeline_id and not pipeline_slug:
        pipeline_slug = 'null'  # get template evaluators

    response = api.v2_evaluators_get({
        "pipelineId": pipeline_id,
        "pipelineSlug": pipeline_slug
    })

    evaluators = response.body.get("data", [])

    return evaluators


def get_test_cases(
        pipeline_id: Optional[str] = None,
        pipeline_slug: Optional[str] = None,
        dataset_id: Optional[str] = None,
) -> List[TestCase]:
    """
    Retrieves test cases for a given dataset ID, pipeline ID, or pipeline slug from the Gentrace API.

    Args:
        dataset_id (str): The ID of the dataset to retrieve test cases for.
        pipeline_id (str): The ID of the pipeline to retrieve test cases for.
        pipeline_slug (str): The pipeline slug to retrieve test cases for.

    Raises:
        ValueError: If the SDK is not initialized. Call init() first.
        ValueError: If neither dataset_id, pipeline_id, nor pipeline_slug is provided.

    Returns:
        list: A list of test cases.
    """

    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    if not dataset_id and not pipeline_id and not pipeline_slug:
        raise ValueError("Either dataset_id, pipeline_id, or pipeline_slug must be defined.")

    if dataset_id:
        response = api.v1_test_case_get({"datasetId": dataset_id})
    else:
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

            pipeline_id = matching_pipeline.get("id")

        params = {}
        if pipeline_id:
            params["pipelineId"] = pipeline_id
        elif pipeline_slug:
            params["pipelineSlug"] = pipeline_slug

        response = api.v1_test_case_get(params)

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
        pipeline_slug: Optional[str] = None,
        payload: List[TestCaseDict] = [],
        dataset_id: Optional[str] = None
) -> int:
    """Creates multiple test cases for a specified pipeline using the Gentrace API.

    Parameters:
    - pipeline_slug (Optional[str]): The unique identifier of the pipeline to which the test cases should be added.
    - payload (List[TestCaseDict]): The array payload containing the test cases to be created.
    - dataset_id (Optional[str]): The unique identifier of the dataset to which the test cases should be added.

    Returns:
    - int: Count of test cases created.

    Raises:
    - ValueError: If the Gentrace API key is not initialized, if neither pipeline_slug nor dataset_id is provided,
                  or if the payload list is empty.

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    If both pipeline_slug and dataset_id are provided, dataset_id will be prioritized.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    if not payload:
        raise ValueError("Payload list cannot be empty")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    if not dataset_id and not pipeline_slug:
        raise ValueError("Either pipeline_slug or dataset_id must be provided")

    request_payload = {"testCases": payload}
    if dataset_id:
        request_payload["datasetId"] = dataset_id
    elif pipeline_slug:
        request_payload["pipelineSlug"] = pipeline_slug

    response = api.v1_test_case_post(request_payload)
    count = response.body.get("creationCount", None)
    return count

def create_test_case(
        pipeline_slug: Optional[str] = None,
        payload: Optional[SingleTestCasePayload] = None,
        dataset_id: Optional[str] = None
) -> str:
    """
    Creates a single test case for a specified pipeline or dataset using the Gentrace API.

    Parameters:
    - payload (SingleTestCasePayload): The payload containing the test case to be created.
    - pipeline_slug (Optional[str]): The unique identifier of the pipeline to which the test case should be added.
    - dataset_id (Optional[str]): The unique identifier of the dataset to which the test case should be added.

    Returns:
    - str: The identifier (caseId) of the created test case.

    Raises:
    - ValueError: If the Gentrace API key is not initialized, if neither pipeline_slug nor dataset_id is provided,
                  or if the payload is not provided.

    Note:
    Ensure that the Gentrace API is initialized by calling init() before using this function.
    If both pipeline_slug and dataset_id are provided, dataset_id will be prioritized.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    if payload is None:
        raise ValueError("Payload must be provided")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    if not dataset_id and not pipeline_slug:
        raise ValueError("Either pipeline_slug or dataset_id must be provided")

    request_payload = {**payload}
    if dataset_id:
        request_payload["datasetId"] = dataset_id
    elif pipeline_slug:
        request_payload["pipelineSlug"] = pipeline_slug

    response = api.v1_test_case_post(request_payload)
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


def delete_test_case(test_case_id: str) -> bool:
    """
    Deletes a test case using the Gentrace API.

    Args:
        test_case_id (str): The ID of the test case to delete.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        bool: True if the test case was successfully deleted, False otherwise.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V2Api(api_client=api_client)

    response = api.v2_test_cases_id_delete(path_params={"id": test_case_id})
    return response.body.get("success", False)


def submit_prepared_test_runs(
        pipeline_slug: str,
        test_runs: List[Dict],
        context: Optional[ResultContext] = None,
        result_name: Optional[str] = None,
) -> Result:
    """
    INTERNAL TO PACKAGE:

    Submits prepared test runs to the Gentrace API for a given pipeline ID. This method requires that you
    create TestRun objects yourself. We recommend using the submit_test_result method instead.

    Args:
        pipeline_slug (str): The pipeline slug
        test_runs (List[Dict]): A list of test runs to submit.
        context (Optional[ResultContext]): Context key pairs
        result_name (str, optional): The name of the test result. Defaults to None.

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

    params = construct_submission_payload(
        pipeline_slug, test_runs, context, result_name
    )
    response = api.v1_test_result_simple_post(params)
    return response.body


def construct_submission_payload(
        pipeline_identifier: str,
        test_runs: List[Dict],
        context: Optional[ResultContext] = None,
        result_name: Optional[str] = None,
):
    """
    Constructs a dictionary payload for submitting test runs to a server.

    Args:
        pipeline_identifier (str): The pipeline slug, or pipeline ID
        test_results (List[Dict]): A list of dictionaries containing test results.
        context (Optional[ResultContext]): Context key pairs
        result_name (str, optional): The name of the test result. Defaults to None.

    Returns:
        Dict: A dictionary payload containing the pipeline slug, test runs, and optional branch and commit information.
    """
    params = {
        "testRuns": test_runs,
    }

    if is_valid_uuid(pipeline_identifier):
        params["pipelineId"] = pipeline_identifier
    else:
        params["pipelineSlug"] = pipeline_identifier

    if GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"]:
        params["name"] = GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"]

    if GENTRACE_CONFIG_STATE["GENTRACE_RESULT_NAME"]:
        params["name"] = GENTRACE_CONFIG_STATE["GENTRACE_RESULT_NAME"]

    if result_name:
        params["name"] = result_name

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
        context: Optional[ResultContext] = None,
        result_name: Optional[str] = None,
) -> Result:
    """
    Submits a test result by creating TestRun objects from given test cases and corresponding outputs.
    To use a Gentrace runner to capture intermediate steps, use run_test instead.

    Args:
        pipeline_slug (str): The pipeline slug
        test_cases (List[TestCase]): A list of TestCase objects.
        outputs_list (List[Dict[str, Any]]): A list of outputs corresponding to each TestCase.
        result_name (str, optional): The name of the test result. Defaults to None.

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
            "inputs": (
                json.loads(test_case["inputs"])
                if isinstance(test_case["inputs"], str)
                else test_case["inputs"]
            ),
            "outputs": outputs,
        }

        test_runs.append(result)

    return submit_prepared_test_runs(pipeline_slug, test_runs, context, result_name)


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

    result = api.v2_evaluations_bulk_post({"data": payloads})

    count = result.body.get("count", None)
    return count

def run_test(
        pipeline_slug: str,
        handler,
        context: Optional[ResultContext] = None,
        case_filter: Optional[Callable[[TestCase], bool]] = None,
        result_name: Optional[str] = None,
        dataset_id: Optional[str] = None,
) -> Result:
    """
    Runs a test by pulling down test cases from Gentrace, running them through †he
    provided callback (once per test case), and submitting the result report back to Gentrace.

    Args:
        pipeline_slug (str): The slug of the pipeline to run.
        handler (Callable[[TestCase], List[Dict]]): A function that takes a TestCase and returns a tuple of
          the output and a PipelineRun class instance that contains the list of steps taken by the pipeline.
        context (Optional[ResultContext]): Context key pairs
        case_filter: Optional[Callable[[TestCase], bool]] = None
        result_name (str, optional): The name of the test result. Defaults to None.
        dataset_id (str, optional): The ID of the dataset to retrieve test cases for. Defaults to None.

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

        if dataset_id:
            test_cases = get_test_cases(dataset_id=dataset_id)
        else:
            test_cases = get_test_cases(pipeline_id=matching_pipeline["id"])

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

        params = construct_submission_payload(
            matching_pipeline["id"], test_runs, context, result_name
        )
        params["collectionMethod"] = "runner"

        response = api.v1_test_result_post(params)

        return response.body
    except Exception as e:
        raise e
    finally:
        decrement_test_counter()

        # OK to flush here and introduce more latency since this is just used for test anyway
        flush()


def get_test_runners(
    pipeline: Pipeline,
    dataset_id: Optional[str] = None,
    case_filter: Optional[Callable[[Dict[str, Any]], bool]] = None
) -> List[Tuple[PipelineRun, Dict[str, Any]]]:
    """
    Retrieves test runners for a given pipeline

    Args:
        pipeline (Pipeline): The pipeline instance
        dataset_id (Optional[str]): Optional dataset ID to filter test cases by.
        case_filter (Optional[Callable[[Dict[str, Any]], bool]]): Optional function to filter test cases

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        A list of (PipelineRun, TestCase) tuples
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V1Api(api_client=api_client)

    if not pipeline:
        raise ValueError("Invalid pipeline found")

    params = {}
    if dataset_id:
        params["datasetId"] = dataset_id
    if is_valid_uuid(pipeline.id):
        params["pipelineId"] = pipeline.id
    else:
        params["pipelineSlug"] = pipeline.slug

    response = api.v1_test_case_get(params)
    test_cases = response.body.get("testCases", [])

    test_runners = []
    total_test_cases = len(test_cases)
    filtered_test_cases = 0

    for test_case in test_cases:
        if case_filter and not case_filter(test_case):
            continue

        filtered_test_cases += 1
        pipeline_run = pipeline.start()
        test_runners.append((pipeline_run, test_case))

    return test_runners

def submit_test_runners(
        pipeline: Pipeline,
        pipeline_run_test_cases: List[Tuple[PipelineRun, TestCase]],
        context: Optional[ResultContext] = None,
        case_filter: Optional[Callable[[TestCase], bool]] = None,
        result_name: Optional[str] = None,
) -> Result:
    """
    Submits test runners for a given pipeline

    Args:
        pipeline (Pipeline): The pipeline instance
        pipeline_run_test_cases (List[Tuple[PipelineRun, TestCase]]): A list of (PipelineRun, TestCase) tuples
        context (Optional[ResultContext]): Context key pairs
        case_filter: Optional[Callable[[TestCase], bool]] = None
        result_name (str, optional): The name of the test result. Defaults to None.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        Response data from the Gentrace API's /test-result POST method. This should just be a dictionary
        similar to the following:

        {
            "resultId": "161c623d-ee92-417f-823a-cf9f7eccf557",
        }
    """
    try:
        config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
        if not config:
            raise ValueError("Gentrace API key not initialized. Call init() first.")

        api_client = ApiClient(configuration=config)
        api = V1Api(api_client=api_client)

        if not pipeline:
            raise ValueError("Invalid pipeline found")

        test_runs = []

        for pipeline_run, test_case in pipeline_run_test_cases:
            if case_filter and not case_filter(test_case):
                continue

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

        params = construct_submission_payload(
            pipeline.id or pipeline.slug, test_runs, context, result_name
        )
        params["collectionMethod"] = "runner"

        response = api.v1_test_result_post(params)
        return response.body
    except Exception as e:
        raise e


class DatasetV2(TypedDict):
    id: str
    name: str
    description: Optional[str]
    pipelineId: str
    createdAt: datetime
    updatedAt: datetime
    archivedAt: Optional[datetime]


class CreateDatasetV2(TypedDict):
    name: str
    description: Optional[str]
    pipelineId: str


class UpdateDatasetV2(TypedDict, total=False):
    name: Optional[str]
    description: Optional[str]
    archived: Optional[bool]


class DatasetListResponse(TypedDict):
    data: List[DatasetV2]


def get_datasets(
        pipeline_slug: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        archived: Optional[bool] = None
) -> DatasetListResponse:
    """
    Get datasets from the Gentrace API, optionally filtered by pipeline slug, pipeline ID, or archived status.

    Args:
        pipeline_slug (str, optional): The slug of the pipeline to filter datasets by. Defaults to None.
        pipeline_id (str, optional): The ID of the pipeline to filter datasets by. Defaults to None.
        archived (bool, optional): Filter datasets by archived status. Defaults to None.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        DatasetListResponse: The response containing an array of datasets returned by the Gentrace API.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V2Api(api_client=api_client)

    query_params = {}
    if pipeline_slug:
        query_params["pipelineSlug"] = pipeline_slug
    if pipeline_id:
        query_params["pipelineId"] = pipeline_id
    if archived is not None:
        query_params["archived"] = archived

    response = api.v2_datasets_get(
        query_params=query_params,
    )
    return DatasetListResponse(data=response.body.get("data", []))


def create_dataset(dataset_data: CreateDatasetV2) -> DatasetV2:
    """
    Create a new dataset using the Gentrace API.

    Args:
        dataset_data (CreateDatasetV2): The data for creating the new dataset.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        DatasetV2: The created dataset returned by the Gentrace API.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V2Api(api_client=api_client)

    response = api.v2_datasets_post(
        body=dataset_data,
    )
    return DatasetV2(**response.body)


def get_dataset(dataset_id: str) -> DatasetV2:
    """
    Get a single dataset from the Gentrace API by its ID.

    Args:
        dataset_id (str): The ID of the dataset to retrieve.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        DatasetV2: The dataset returned by the Gentrace API.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V2Api(api_client=api_client)

    response = api.v2_datasets_id_get(
        path_params={"id": dataset_id}
    )
    return DatasetV2(**response.body)


def update_dataset(dataset_id: str, update_data: UpdateDatasetV2) -> DatasetV2:
    """
    Update an existing dataset using the Gentrace API.

    Args:
        dataset_id (str): The ID of the dataset to update.
        update_data (UpdateDatasetV2): The data for updating the dataset.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        DatasetV2: The updated dataset returned by the Gentrace API.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = V2Api(api_client=api_client)

    response = api.v2_datasets_id_post(
        body=update_data,
        path_params={"id": dataset_id}
    )
    return DatasetV2(**response.body)


def update_test_result_with_runners(
        result_id: str,
        pipeline_run_test_cases: List[Tuple[PipelineRun, TestCase]],
) -> Dict[str, Any]:
    """
    Updates a test result with additional test runs.

    Args:
        result_id (str): The ID of the test result to update.
        pipeline_run_test_cases (List[Tuple[PipelineRun, TestCase]]): A list of (PipelineRun, TestCase) tuples
            representing additional test runs to add to the existing test result.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        Dict[str, Any]: Response data from the Gentrace API's /test-result/{id} POST method.
    """
    try:
        config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
        if not config:
            raise ValueError("Gentrace API key not initialized. Call init() first.")

        api_client = ApiClient(configuration=config)
        api = V1Api(api_client=api_client)

        test_runs = []

        for pipeline_run, test_case in pipeline_run_test_cases:
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

                step_run_data = {
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

                if step_run.error:
                    step_run_data["error"] = step_run.error

                step_runs_data.append(step_run_data)

            test_run = {
                "caseId": test_case["id"],
                "metadata": merged_metadata,
                "previousRunId": pipeline_run.context.get("previousRunId"),
                "stepRuns": step_runs_data,
            }

            if pipeline_run.get_error():
                test_run["error"] = pipeline_run.get_error()

            if "name" in test_case:
                test_run["name"] = test_case["name"]
            
            if "inputs" in test_case:
                test_run["inputs"] = test_case["inputs"]

            if pipeline_run.get_id():
                test_run["id"] = pipeline_run.get_id()

            test_runs.append(test_run)

        response = api.v1_test_result_id_post(
            path_params={"id": result_id},
            body={"testRuns": test_runs}
        )
        return response.body
    except Exception as e:
        raise e


__all__ = [
    "get_evaluators",
    "get_test_cases",
    "get_test_case",
    "create_test_cases",
    "create_test_case",
    "delete_test_case",
    "get_test_results",
    "get_test_result",
    "update_test_case",
    "submit_test_result",
    "get_pipelines",
    "construct_submission_payload",
    "run_test",
    "get_test_runners",
    "submit_test_runners",
    "bulk_create_evaluations",
    "update_test_result_with_runners",
    "OutputStep",
    "EvaluationDict",
    "get_dataset",
    "update_dataset",
    "create_dataset",
    "get_datasets",
]
