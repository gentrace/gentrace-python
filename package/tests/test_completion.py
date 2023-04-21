import http.client
import json
import os
import re
import uuid
from unittest.mock import create_autospec

import aiohttp
import openai
import pytest
import requests
from aioresponses import CallbackResult, aioresponses
from urllib3.response import HTTPResponse

import gentrace

gentrace.configure_openai()


def test_openai_completion_self_contained_pipeline_id(
    mocker, completion_response, gentrace_pipeline_run_response
):
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

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
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

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
