from typing import Dict, TypedDict

from gentrace.providers.init import (
    GENTRACE_CONFIG_STATE,
)


class Run(TypedDict):
    runId: str


def get_test_cases(set_id: str):
    api = GENTRACE_CONFIG_STATE["global_gentrace_api"]
    if not api:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    response = api.test_case_get({"setId": set_id})
    data = response.body
    return data["testCases"]


def submit_test_results(set_id: str, test_results: list[Dict]) -> Run:
    api = GENTRACE_CONFIG_STATE["global_gentrace_api"]
    if not api:
        raise ValueError("Gentrace API key not initialized. Call init() first.")

    params = {
        "setId": set_id,
        "testResults": test_results,
    }

    if GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"]:
        params["branch"] = GENTRACE_CONFIG_STATE["GENTRACE_BRANCH"]

    if GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"]:
        params["commit"] = GENTRACE_CONFIG_STATE["GENTRACE_COMMIT"]

    response = api.test_run_post(params)
    data = response.body
    return data


__all__ = [
    "get_test_cases",
    "submit_test_results",
]
