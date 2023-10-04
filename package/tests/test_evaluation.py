import http.client
import json
import os
import uuid
from typing import Any, List
from unittest.mock import create_autospec

import pytest
import requests
import responses
from responses import matchers
from urllib3.response import HTTPResponse

import gentrace
from gentrace.providers.evaluation import OutputStep, construct_submission_payload
from gentrace.providers.init import GENTRACE_CONFIG_STATE
from gentrace.providers.utils import get_test_counter


def test_evaluation_get_test_cases(
    mocker, test_cases, setup_teardown_openai, pipelines
):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_cases, ensure_ascii=False).encode("utf-8")

    gentrace_response_tc = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    pipeline_body = json.dumps(pipelines, ensure_ascii=False).encode("utf-8")

    gentrace_response_pipelines = HTTPResponse(
        body=pipeline_body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.side_effect = [gentrace_response_pipelines, gentrace_response_tc]

    test_cases = gentrace.get_test_cases(pipeline_slug="guess-the-year")

    assert len(test_cases) == 3


def test_evaluation_create_test_cases(
    mocker, setup_teardown_openai, multiple_create_tc
):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(multiple_create_tc, ensure_ascii=False).encode("utf-8")

    gentrace_response_creation_count = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.side_effect = [
        gentrace_response_creation_count,
    ]

    response = gentrace.create_test_cases(
        pipeline_slug="guess-the-year",
        payload=[
            {
                "name": "Test case 1",
                "inputs": {"a": "1", "b": "2"},
                "expectedOutputs": {"value": "3"},
            },
            {
                "name": "Test case 2",
                "inputs": {"a": "1", "b": "2"},
                "expectedOutputs": {"value": "3"},
            },
        ],
    )

    assert response == 2


def test_evaluation_create_test_case(mocker, setup_teardown_openai, single_create_tc):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(single_create_tc, ensure_ascii=False).encode("utf-8")

    gentrace_response_creation_count = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.side_effect = [
        gentrace_response_creation_count,
    ]

    response = gentrace.create_test_case(
        pipeline_slug="guess-the-year",
        payload={
            "name": "Test case 1",
            "inputs": {"a": "1", "b": "2"},
            "expectedOutputs": {"value": "3"},
        },
    )

    assert response == "550e8400-e29b-41d4-a716-446655440000"


def test_evaluation_update_test_case(mocker, setup_teardown_openai, update_tc):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(update_tc, ensure_ascii=False).encode("utf-8")

    gentrace_response_creation_count = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.side_effect = [
        gentrace_response_creation_count,
    ]

    response = gentrace.update_test_case(
        pipeline_slug="guess-the-year",
        payload={
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Test case 1",
        },
    )

    assert response == "550e8400-e29b-41d4-a716-446655440000"


def test_evaluation_submit_test_run_pipeline_slug(
    mocker, test_cases, setup_teardown_openai, test_result_response_simple, pipelines
):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_cases, ensure_ascii=False).encode("utf-8")

    gentrace_response_tc = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    pipeline_body = json.dumps(pipelines, ensure_ascii=False).encode("utf-8")

    gentrace_response_pipelines = HTTPResponse(
        body=pipeline_body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.side_effect = [gentrace_response_pipelines, gentrace_response_tc]

    test_cases = gentrace.get_test_cases(
        pipeline_id="201196DC-9471-4B28-A051-C21AE45F247A"
    )

    runs = []
    for case in test_cases:
        runs.append(
            {
                "value": "This is an output",
            }
        )

    # Setup Gentrace mocked response for submit_test_run
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_result_response_simple, ensure_ascii=False).encode("utf-8")

    gentrace_response_tr = HTTPResponse(
        body=body,
        headers=headers,
        status=200,
        reason="OK",
        preload_content=False,
        decode_content=True,
        enforce_content_length=True,
    )

    gentrace_request = mocker.patch.object(gentrace.api_client.ApiClient, "request")
    gentrace_request.side_effect = [gentrace_response_tr]

    result = gentrace.submit_test_result(
        pipeline_slug="guess-the-year",
        test_cases=test_cases,
        outputs_list=runs,
    )

    assert result["resultId"] == "9685b34e-2cac-5bd2-8751-c9e34ff9fd98"


def test_evaluation_submit_test_run_output_steps(
    mocker, test_cases, setup_teardown_openai, test_result_response_simple
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

    test_cases = gentrace.get_test_cases(
        pipeline_id="201196DC-9471-4B28-A051-C21AE45F247A"
    )

    outputs = []
    for _ in test_cases:
        outputs.append(
            {
                "value": "This is an output",
                "steps": [
                    {
                        "key": "compose",
                        "output": "This is an output",
                        "monkies": "testing",
                    }
                ],
            }
        )

    # Setup Gentrace mocked response for submit_test_run
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(test_result_response_simple, ensure_ascii=False).encode("utf-8")

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

    result = gentrace.submit_test_result(
        pipeline_slug="guess-the-year",
        test_cases=test_cases,
        outputs_list=outputs,
    )

    assert result["resultId"] == "9685b34e-2cac-5bd2-8751-c9e34ff9fd98"


def test_validate_construct_submission_works_with_env():
    os.environ["GENTRACE_BRANCH"] = "test-branch"
    os.environ["GENTRACE_COMMIT"] = "test-commit"

    payload = gentrace.construct_submission_payload("pipeline_slug", [])

    assert payload["branch"] == "test-branch"
    assert payload["commit"] == "test-commit"


def test_validate_construct_submission_works_with_init():
    gentrace.init(api_key="sldkjflk", branch="test-branch", commit="test-commit")
    payload = gentrace.construct_submission_payload("pipeline_slug", [])

    assert payload["branch"] == "test-branch"
    assert payload["commit"] == "test-commit"


def test_validate_construct_submission_prioritizes_override():
    os.environ["GENTRACE_BRANCH"] = "test-branch-env"
    os.environ["GENTRACE_COMMIT"] = "test-commit-env"

    gentrace.init(
        api_key="test-api-key", branch="test-branch-init", commit="test-commit-init"
    )
    payload = gentrace.construct_submission_payload("pipeline_slug", [])

    assert payload["branch"] == "test-branch-init"
    assert payload["commit"] == "test-commit-init"


def test_prioritize_gentrace_result_name_over_gentrace_run_name(setup_teardown_openai):
    os.environ["GENTRACE_RUN_NAME"] = ""
    os.environ["GENTRACE_RESULT_NAME"] = ""

    os.environ["GENTRACE_RESULT_NAME"] = "result-name"
    os.environ["GENTRACE_RUN_NAME"] = "run-name"

    gentrace.init(
        api_key="gentrace-api-key",
    )

    payload = gentrace.construct_submission_payload("pipeline-id", [])

    assert payload["name"] == "result-name"


def test_should_still_read_gentrace_run_name(setup_teardown_openai):
    os.environ["GENTRACE_RUN_NAME"] = ""
    os.environ["GENTRACE_RESULT_NAME"] = ""

    os.environ["GENTRACE_RUN_NAME"] = "run-name"

    gentrace.init(
        api_key="gentrace-api-key",
    )

    payload = gentrace.construct_submission_payload("pipeline-id", [])

    assert payload["name"] == "run-name"


def test_should_read_gentrace_result_name(setup_teardown_openai):
    os.environ["GENTRACE_RUN_NAME"] = ""
    os.environ["GENTRACE_RESULT_NAME"] = ""

    os.environ["GENTRACE_RESULT_NAME"] = "result-name"

    gentrace.init(
        api_key="gentrace-api-key",
    )

    payload = gentrace.construct_submission_payload("pipeline-id", [])

    assert payload["name"] == "result-name"


def test_should_read_result_name_over_run_name(setup_teardown_openai):
    os.environ["GENTRACE_RUN_NAME"] = ""
    os.environ["GENTRACE_RESULT_NAME"] = ""

    gentrace.init(
        api_key="gentrace-api-key",
        run_name="run-name",
        result_name="result-name"
    )

    payload = gentrace.construct_submission_payload("pipeline-id", [])

    assert payload["name"] == "result-name"


def test_should_still_read_run_name(setup_teardown_openai):
    os.environ["GENTRACE_RUN_NAME"] = ""
    os.environ["GENTRACE_RESULT_NAME"] = ""

    gentrace.init(
        api_key="gentrace-api-key",
        run_name="run-name"
    )

    payload = gentrace.construct_submission_payload("pipeline-id", [])

    assert payload["name"] == "run-name"


def test_should_read_result_name(setup_teardown_openai):
    os.environ["GENTRACE_RUN_NAME"] = ""
    os.environ["GENTRACE_RESULT_NAME"] = ""

    gentrace.init(
        api_key="gentrace-api-key",
        result_name="result-name"
    )

    payload = gentrace.construct_submission_payload("pipeline-id", [])

    assert payload["name"] == "result-name"


def test_evaluation_get_pipelines(mocker, pipelines, setup_teardown_openai):
    # Setup Gentrace mocked response for get_test_cases
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(pipelines, ensure_ascii=False).encode("utf-8")

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

    pipelines = gentrace.get_pipelines()

    assert len(pipelines) == 2


def test_evaluation_measure(mocker, setup_teardown_openai, test_result_response):
    pipeline = gentrace.Pipeline(
        "guess-the-year",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    def create_measure_callback(test_case):
        runner = pipeline.start()
        output = runner.measure(lambda x=5, y=3: x + y, x=100, y=1000)
        return [output, runner]

    result = gentrace.run_test("guess-the-year", create_measure_callback)

    print("Result: ", result)


def test_evaluation_measure_validate_steps(
    mocker, setup_teardown_openai, test_result_response
):
    pipeline = gentrace.Pipeline(
        "guess-the-year",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner_list = []

    def create_measure_callback(test_case):
        runner = pipeline.start()
        output = runner.measure(lambda x=5, y=3: x + y, x=100, y=1000)

        runner_list.append(runner)

        return [output, runner]

    response = gentrace.run_test("guess-the-year", create_measure_callback)

    assert response.get("resultId", None) is not None

    for runner in runner_list:
        assert len(runner.step_runs) == 1
        assert runner.step_runs[0].outputs == {"value": 1100}


def test_evaluation_checkpoint(mocker, setup_teardown_openai, test_result_response):
    pipeline = gentrace.Pipeline(
        "guess-the-year",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner_list = []

    def create_checkpoint_callback(test_case):
        runner = pipeline.start()
        runner.checkpoint({"inputs": {"x": 100, "y": 1000}, "outputs": {"value": 1100}})
        runner.checkpoint({"inputs": {"x": 100, "y": 1000}, "outputs": {"value": 1100}})
        runner_list.append(runner)

        return ["something", runner]

    response = gentrace.run_test("guess-the-year", create_checkpoint_callback)

    assert response.get("resultId", None) is not None

    for runner in runner_list:
        assert len(runner.step_runs) == 2
        assert runner.step_runs[0].outputs == {"value": 1100}


def test_evaluation_counter_rest(mocker, setup_teardown_openai, test_result_response):
    pipeline = gentrace.Pipeline(
        "guess-the-year",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner_list = []

    def create_checkpoint_callback(test_case):
        runner = pipeline.start()
        runner.checkpoint({"inputs": {"x": 100, "y": 1000}, "outputs": {"value": 1100}})
        runner.checkpoint({"inputs": {"x": 100, "y": 1000}, "outputs": {"value": 1100}})
        runner_list.append(runner)

        return ["something", runner]

    assert get_test_counter() == 0

    response = gentrace.run_test("guess-the-year", create_checkpoint_callback)

    assert get_test_counter() == 0

    assert response.get("resultId", None) is not None

    for runner in runner_list:
        assert len(runner.step_runs) == 2
        assert runner.step_runs[0].outputs == {"value": 1100}


def test_evaluation_counter_rest_when_run_test_fails(
    mocker, setup_teardown_openai, test_result_response
):
    pipeline = gentrace.Pipeline(
        "guess-the-year",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner_list = []

    def create_checkpoint_callback(test_case):
        runner = pipeline.start()
        runner.checkpoint({"inputs": {"x": 100, "y": 1000}, "outputs": {"value": 1100}})
        runner.checkpoint({"inputs": {"x": 100, "y": 1000}, "outputs": {"value": 1100}})
        runner_list.append(runner)

        return ["something", runner]

    assert get_test_counter() == 0

    try:
        gentrace.run_test("random-slug-no-exist", create_checkpoint_callback)
    except Exception as e:
        pass

    assert get_test_counter() == 0
