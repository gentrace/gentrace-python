from typing import Dict, TypedDict

from gentrace.providers.init import (
    GENTRACE_BRANCH,
    GENTRACE_COMMIT,
    global_gentrace_api,
)


class Run(TypedDict):
    runId: str


def get_test_cases(set_id: str):
    if not global_gentrace_api:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    response = global_gentrace_api.test_case_get({"setId": set_id})
    data = response.body
    return data["testCases"]


def submit_test_results(set_id: str, test_results: list[Dict]) -> Run:
    if not global_gentrace_api:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    params = {
        "setId": set_id,
        "testResults": test_results,
    }

    if GENTRACE_BRANCH:
        params["branch"] = GENTRACE_BRANCH

    if GENTRACE_COMMIT:
        params["commit"] = GENTRACE_COMMIT

    response = global_gentrace_api.test_run_post(params)
    data = response.body
    return data


__all__ = [
    "get_test_cases",
    "submit_test_results",
]
