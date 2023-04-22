import http.client
import io
import json
import os
import re
import uuid
from unittest.mock import create_autospec

import aiohttp
import openai
import pytest
import requests
import responses
from aioresponses import CallbackResult, aioresponses
from urllib3.response import HTTPResponse

import gentrace

gentrace.api_key = os.getenv("GENTRACE_API_KEY")
gentrace.host = "http://localhost:3000/api/v1"

gentrace.configure_openai()


def test_openai_completion_self_contained_pipeline_id(
    mocker, completion_response, gentrace_pipeline_run_response
):
    openai.api_key = os.getenv("OPENAI_KEY")

    # Setup OpenAI mocked request
    openai_api_key_getter = mocker.patch.object(openai.util, "default_api_key")
    openai_api_key_getter.return_value = "test-key"

    openai_request = mocker.patch.object(requests.sessions.Session, "request")

    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = json.dumps(completion_response, ensure_ascii=False).encode(
        "utf-8"
    )

    openai_request.return_value = response

    # Setup Gentrace mocked response
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )

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

    result = openai.Completion.create(
        pipeline_id="text-generation",
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
    )

    assert uuid.UUID(result.pipeline_run_id) is not None


def test_openai_completion_self_contained_no_pipeline_id(
    mocker, completion_response, gentrace_pipeline_run_response
):
    openai.api_key = os.getenv("OPENAI_KEY")

    # Setup OpenAI mocked request
    openai_api_key_getter = mocker.patch.object(openai.util, "default_api_key")
    openai_api_key_getter.return_value = "test-key"

    openai_request = mocker.patch.object(requests.sessions.Session, "request")

    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = json.dumps(completion_response, ensure_ascii=False).encode(
        "utf-8"
    )

    openai_request.return_value = response

    # Setup Gentrace mocked response
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )

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

    result = openai.Completion.create(
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
    )

    assert not hasattr(result, "pipeline_run_id")


@pytest.mark.asyncio
async def test_openai_completion_self_contained_no_pipeline_id_async(
    mocker, mockaio, completion_response, gentrace_pipeline_run_response
):
    # Setup OpenAI mocked request
    pattern = re.compile(r"^https://api\.openai\.com/v1/.*$")
    mockaio.post(
        pattern,
        status=200,
        body=json.dumps(completion_response, ensure_ascii=False).encode("utf-8"),
    )

    # Setup Gentrace mocked response
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )

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

    result = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
    )

    assert not hasattr(result, "pipeline_run_id")


@pytest.mark.asyncio
async def test_openai_completion_self_contained_pipeline_id_async(
    mocker, mockaio, completion_response, gentrace_pipeline_run_response
):
    # Setup OpenAI mocked request
    pattern = re.compile(r"^https://api\.openai\.com/v1/.*$")
    mockaio.post(
        pattern,
        status=200,
        body=json.dumps(completion_response, ensure_ascii=False).encode("utf-8"),
    )

    # Setup Gentrace mocked response
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )

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

    result = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
        pipeline_id="test_openai_completion_self_contained_no_pipeline_id_async",
    )

    assert uuid.UUID(result.pipeline_run_id) is not None


@responses.activate
def test_openai_completion_self_contained_pipeline_id_stream(
    mocker, completion_response, gentrace_pipeline_run_response
):
    openai.api_key = os.getenv("OPENAI_KEY")

    # Setup OpenAI mocked request
    openai_api_key_getter = mocker.patch.object(openai.util, "default_api_key")
    openai_api_key_getter.return_value = "test-key"

    responses.add(
        responses.POST,
        "https://api.openai.com/v1/completions",
        body="data: " + json.dumps(completion_response, ensure_ascii=False),
        stream=True,
        content_type="text/event-stream",
    )

    # Setup Gentrace mocked response
    headers = http.client.HTTPMessage()
    headers.add_header("Content-Type", "application/json")

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )

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

    result = openai.Completion.create(
        pipeline_id="text-generation",
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
        stream=True,
    )

    print("Before")
    pipeline_run_id = None
    for value in result:
        print("Getting stream value", value)
        pipeline_run_id = value["pipeline_run_id"]
    print("After")

    assert uuid.UUID(pipeline_run_id) is not None
