import json
import os
import uuid
from itertools import zip_longest
from typing import Any, Dict, List, Optional, TypedDict, Union

from gentrace.api_client import ApiClient
from gentrace.apis.tags.core_api import CoreApi
from gentrace.model.test_case import TestCase
from gentrace.models import CreateMultipleTestCases
from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)
from gentrace.providers.pipeline_run import flush
from gentrace.providers.utils import (
    decrement_test_counter,
    get_test_counter,
    increment_test_counter,
)


class Run(TypedDict):
    runId: str


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
) -> List[TestCaseDict]:
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
    api = CoreApi(api_client=api_client)

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

    response = api.test_case_get({"pipelineId": effective_pipeline_id})
    test_cases = response.body.get("testCases", [])
    return test_cases


class CreateTestCasePayload(TypedDict):
    name: str
    inputs: Dict[str, Any]
    expectedOutputs: Optional[Dict[str, Any]]


class MultipleTestCasesPayload(TypedDict):
    testCases: List[TestCaseDict]


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
    payload: MultipleTestCasesPayload,
) -> int:
    """Creates multiple test cases for a specified pipeline using the Gentrace API.

    Parameters:
    - pipeline_slug (str): The unique identifier of the pipeline to which the test cases should be added.
    - payload (MultipleTestCasesPayload): The payload containing the test cases to be created.

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
    api = CoreApi(api_client=api_client)

    if not pipeline_slug:
        raise ValueError("pipeline_slug must be passed")

    response = api.test_case_post(
        {"pipelineSlug": pipeline_slug, "testCases": payload["testCases"]}
    )
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
    api = CoreApi(api_client=api_client)

    if not pipeline_slug:
        raise ValueError("pipeline_slug must be passed")

    response = api.test_case_post({"pipelineSlug": pipeline_slug, **payload})
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
    api = CoreApi(api_client=api_client)

    if not pipeline_slug:
        raise ValueError("pipeline_slug must be passed")

    response = api.test_case_patch({"pipelineSlug": pipeline_slug, **payload})
    case_id = response.body.get("caseId", None)
    return case_id


def submit_prepared_test_results(set_id: str, test_results: List[Dict]) -> Run:
    """
    DEPRECATED - use run_test (advanced runner use case) or submit_test_result (basic use case) instead.
    Submits prepared test results to the Gentrace API for a given set ID. This method requires that you
    create TestResult objects yourself. We recommend using the submitTestResults method instead.

    Args:
        set_id (str): The ID of the test set associated with the test results.
        test_results (List[Dict]): A list of test results to submit.

    Raises:
        ValueError: If the SDK is not initialized. Call init() first.

    Returns:
        Run: The response data from the API.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    api_client = ApiClient(configuration=config)
    api = CoreApi(api_client=api_client)

    for test_result in test_results:
        test_result["inputs"] = (
            json.dumps(test_result["inputs"])
            if isinstance(test_result["inputs"], str)
            else test_result["inputs"]
        )

    params = construct_submission_payload(set_id, test_results)
    response = api.test_run_post(params)
    return response.body


def construct_submission_payload(set_id: str, test_results: List[Dict]):
    """
    Constructs a dictionary payload for submitting test results to a server.

    Args:
        set_id (str): The ID of the test set.
        test_results (List[Dict]): A list of dictionaries containing test results.

    Returns:
        Dict: A dictionary payload containing the set ID, test results, and optional branch and commit information.
    """
    params = {
        "setId": set_id,
        "testResults": test_results,
    }

    if GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"]:
        params["name"] = GENTRACE_CONFIG_STATE["GENTRACE_RUN_NAME"]

    if os.getenv("GENTRACE_BRANCH") or GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"]:
        params["branch"] = GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"] or os.getenv(
            "GENTRACE_BRANCH"
        )

    if os.getenv("GENTRACE_COMMIT") or GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"]:
        params["commit"] = GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"] or os.getenv(
            "GENTRACE_COMMIT"
        )

    return params


class OutputStep(TypedDict):
    key: str
    output: str
    inputs: Optional[Dict[str, Any]]


def submit_test_result(
    pipeline_slug: str,
    test_cases: List[TestCase],
    outputs_list: List[Dict[str, Any]],
) -> Run:
    """
    Submits a test result by creating TestResult objects from given test cases and corresponding outputs.
    To use a Gentrace runner to capture intermediate steps, use run_test instead.

    Args:
        pipeline_slug (str): The pipeline slug
        test_cases (List[TestCase]): A list of TestCase objects.
        outputs_list (List[Dict[str, Any]]): A list of outputs corresponding to each TestCase.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        Run: The response data from the Gentrace API's testRunPost method.
    """
    config = GENTRACE_CONFIG_STATE["global_gentrace_config"]
    if not config:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    if len(test_cases) != len(outputs_list):
        raise ValueError("`test_cases` and `outputs` should be the same length.")

    test_results = []

    for test_case, outputs in zip_longest(test_cases, outputs_list, fillvalue=None):
        result = {
            "caseId": test_case["id"],
            "inputs": json.loads(test_case["inputs"])
            if isinstance(test_case["inputs"], str)
            else test_case["inputs"],
            "outputs": outputs,
        }

        test_results.append(result)

    pipeline_id = pipeline_slug

    if not is_valid_uuid(pipeline_slug):
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

    return submit_prepared_test_results(pipeline_id, test_results)


def get_pipelines(
    label: Optional[str] = None,
    slug: Optional[str] = None,
) -> Run:
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
    api = CoreApi(api_client=api_client)

    params = {}

    if label:
        params["label"] = label

    if slug:
        params["slug"] = slug

    response = api.pipelines_get(params)

    pipelines = response.body.get("pipelines")

    return pipelines


def run_test(pipeline_slug: str, handler) -> Result:
    """
    Runs a test by pulling down test cases from Gentrace, running them through †he
    provided callback (once per test case), and submitting the result report back to Gentrace.

    Args:
        pipeline_slug (str): The slug of the pipeline to run.
        handler (Callable[[TestCase], List[Dict]]): A function that takes a TestCase and returns a tuple of
          the output and a PipelineRun class instance that contains the list of steps taken by the pipeline.

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
        api = CoreApi(api_client=api_client)

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
            [output, pipeline_run] = handler(test_case)

            test_run = {
                "caseId": test_case["id"],
                "stepRuns": [
                    {
                        "provider": {
                            "name": step_run.provider,
                            "invocation": step_run.invocation,
                            "modelParams": step_run.model_params,
                            "inputs": step_run.inputs,
                            "outputs": step_run.outputs,
                        },
                        "elapsedTime": step_run.elapsed_time,
                        "startTime": step_run.start_time,
                        "endTime": step_run.end_time,
                    }
                    for step_run in pipeline_run.step_runs
                ],
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

        if os.getenv("GENTRACE_BRANCH") or GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"]:
            params["branch"] = GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"] or os.getenv(
                "GENTRACE_BRANCH"
            )

        if os.getenv("GENTRACE_COMMIT") or GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"]:
            params["commit"] = GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"] or os.getenv(
                "GENTRACE_COMMIT"
            )

        params["collectionMethod"] = "runner"

        response = api.test_result_post(params)
        return response.body
    except Exception as e:
        raise e
    finally:
        decrement_test_counter()

        # OK to flush here and introduce more latency since this is just used for test anyway
        flush()


__all__ = [
    "get_test_cases",
    "create_test_cases",
    "create_test_case",
    "update_test_case",
    "submit_test_result",
    "get_pipelines",
    "submit_prepared_test_results",
    "construct_submission_payload",
    "run_test",
    "OutputStep",
]
