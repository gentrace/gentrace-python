import json
from typing import Dict, List, TypedDict

from gentrace.model.test_case import TestCase
from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)


class Run(TypedDict):
    runId: str


def get_test_cases(set_id: str):
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

    params = {
        "setId": set_id,
        "testResults": test_results,
    }

    if GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"]:
        params["branch"] = GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"]

    if GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"]:
        params["commit"] = GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"]

    response = api.test_run_post(params)
    return response.body


def submit_test_results(
    set_id: str, test_cases: List[TestCase], outputs: List[str]
) -> Run:
    """
    Submits test results by creating TestResult objects from given test cases and corresponding outputs.

    Args:
        set_id (str): The identifier of the test set.
        test_cases (List[TestCase]): A list of TestCase objects.
        outputs (List[str]): A list of outputs corresponding to each TestCase.

    Raises:
        ValueError: If the Gentrace API key is not initialized.

    Returns:
        Run: The response data from the Gentrace API's testRunPost method.
    """
    api = GENTRACE_CONFIG_STATE["global_gentrace_api"]
    if not api:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    test_results = [
        {
            "caseId": test_case["id"],
            "inputs": json.loads(test_case["inputs"])
            if isinstance(test_case["inputs"], str)
            else test_case["inputs"],
            "output": output,
        }
        for test_case, output in zip(test_cases, outputs)
    ]

    params = {
        "setId": set_id,
        "testResults": test_results,
    }

    response = api.test_run_post(params)
    return response.body


__all__ = ["get_test_cases", "submit_test_results", "submit_prepared_test_results"]
