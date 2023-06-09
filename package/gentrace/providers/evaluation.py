import json
import os
from itertools import zip_longest
from typing import Any, Dict, List, Optional, TypedDict

from gentrace.model.test_case import TestCase
from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)


class Run(TypedDict):
    runId: str


class TestCaseDict(TypedDict):
    id: str
    createdAt: str
    updatedAt: str
    archivedAt: Optional[str]
    expected: Optional[str]
    inputs: dict[str, Any]
    name: str
    setId: str


def get_test_cases(set_id: str) -> List[TestCaseDict]:
    """
    Retrieves test cases for a given set ID from the Gentrace API.

    Args:
        set_id (str): The ID of the test set to retrieve.

    Raises:
        ValueError: If the SDK is not initialized. Call init() first.

    Returns:
        list: A list of test cases.
    """
    api = GENTRACE_CONFIG_STATE["global_gentrace_api"]
    if not api:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    response = api.test_case_get({"setId": set_id})
    test_cases = response.body.get("testCases", [])
    return test_cases


def submit_prepared_test_results(set_id: str, test_results: list[Dict]) -> Run:
    """
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
    api = GENTRACE_CONFIG_STATE["global_gentrace_api"]
    if not api:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    for test_result in test_results:
        test_result["inputs"] = (
            json.dumps(test_result["inputs"])
            if isinstance(test_result["inputs"], str)
            else test_result["inputs"]
        )

    params = construct_submission_payload(set_id, test_results)
    response = api.test_run_post(params)
    return response.body


def construct_submission_payload(set_id: str, test_results: list[Dict]):
    """
    Constructs a dictionary payload for submitting test results to a server.

    Args:
        set_id (str): The ID of the test set.
        test_results (list[Dict]): A list of dictionaries containing test results.

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
    inputs: Optional[dict[str, Any]]


def submit_test_results(
    set_id: str,
    test_cases: List[TestCase],
    outputs: List[str],
    output_steps: Optional[List[List[OutputStep]]] = [],
) -> Run:
    """
    Submits test results by creating TestResult objects from given test cases and corresponding outputs.

    Args:
        set_id (str): The identifier of the test set.
        test_cases (List[TestCase]): A list of TestCase objects.
        outputs (List[str]): A list of outputs corresponding to each TestCase.
        output_steps (Optional[List[List[OutputStep]]], optional): A list of lists of OutputStep objects. Defaults to [].

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        Run: The response data from the Gentrace API's testRunPost method.
    """
    api = GENTRACE_CONFIG_STATE["global_gentrace_api"]
    if not api:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    if len(test_cases) != len(outputs):
        raise ValueError("`test_cases` and `outputs` should be the same length.")

    test_results = []

    for test_case, output, output_steps_inner in zip_longest(
        test_cases, outputs, output_steps, fillvalue=None
    ):
        result = {
            "caseId": test_case["id"],
            "inputs": json.loads(test_case["inputs"])
            if isinstance(test_case["inputs"], str)
            else test_case["inputs"],
            "output": output,
        }

        # Steps are optional but they can't be null. If they're defined, they must
        # be an array and have at least one step.
        if output_steps_inner:
            result["outputSteps"] = output_steps_inner

        test_results.append(result)

    return submit_prepared_test_results(set_id, test_results)


__all__ = [
    "get_test_cases",
    "submit_test_results",
    "submit_prepared_test_results",
    "construct_submission_payload",
    "OutputStep",
]
