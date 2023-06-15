import http.client
import json
import os
from unittest.mock import create_autospec

import pytest
import requests
from responses import matchers
from urllib3.response import HTTPResponse

import gentrace
from gentrace.providers.init import GENTRACE_CONFIG_STATE


def test_evaluation_get_test_cases(mocker, test_cases, setup_teardown_openai):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_cases, ensure_ascii=False).encode("utf-8")

    gentrace_response = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.return_value = gentrace_response

    test_cases = gentrace.get_test_cases(set_id="201196DC-9471-4B28-A051-C21AE45F247A")


def test_evaluation_submit_test_run(
    mocker, test_cases, setup_teardown_openai, test_run_response
):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_cases, ensure_ascii=False).encode("utf-8")

    gentrace_response = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.return_value = gentrace_response

    test_cases = gentrace.get_test_cases(set_id="201196DC-9471-4B28-A051-C21AE45F247A")

    results = []
    for case in test_cases:
        results.append(
            "This is an output",
        )

    # Setup Gentrace mocked response for submit_test_run
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_run_response, ensure_ascii=False).encode("utf-8")

    gentrace_response = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.return_value = gentrace_response

    result = gentrace.submit_test_results(
        set_id="201196DC-9471-4B28-A051-C21AE45F247A",
        test_cases=test_cases,
        outputs=results,
    )

    print(result)


def test_evaluation_submit_prepared_test_run(
    mocker, test_cases, setup_teardown_openai, test_run_response
):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_cases, ensure_ascii=False).encode("utf-8")

    gentrace_response = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.return_value = gentrace_response

    test_cases = gentrace.get_test_cases(set_id="201196DC-9471-4B28-A051-C21AE45F247A")

    results = []
    for case in test_cases:
        results.append(
            {
                "caseId": case["id"],
                "inputs": {
                    "a": "1",
                    "b": "2",
                },
                "output": "This are some outputs",
            }
        )

    # Setup Gentrace mocked response for submit_test_run
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_run_response, ensure_ascii=False).encode("utf-8")

    gentrace_response = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.return_value = gentrace_response

    result = gentrace.submit_prepared_test_results(
        set_id="201196DC-9471-4B28-A051-C21AE45F247A",
        test_results=results,
    )

    print(result)
