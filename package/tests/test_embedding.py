import http.client
import json
import os
import uuid
from unittest.mock import create_autospec

import openai
import requests
from urllib3.response import HTTPResponse

import gentrace


def test_embedding_self_contained_pipeline_id(
    mocker, embedding_response, gentrace_pipeline_run_response
):
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()

    openai.api_key = os.getenv("OPENAI_KEY")

    # Setup OpenAI mocked request
    openai_api_key_getter = mocker.patch.object(openai.util, "default_api_key")
    openai_api_key_getter.return_value = "test-key"

    openai_request = mocker.patch.object(requests.sessions.Session, "request")

    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = json.dumps(embedding_response, ensure_ascii=False).encode(
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

    result = openai.Embedding.create(
        input="sample text",
        model="text-similarity-davinci-001",
        pipeline_id="testing-value",
    )

    assert uuid.UUID(result.pipeline_run_id) is not None


def test_embedding_self_contained_no_pipeline_id(
    mocker, embedding_response, gentrace_pipeline_run_response
):
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()

    openai.api_key = os.getenv("OPENAI_KEY")

    # Setup OpenAI mocked request
    openai_api_key_getter = mocker.patch.object(openai.util, "default_api_key")
    openai_api_key_getter.return_value = "test-key"

    openai_request = mocker.patch.object(requests.sessions.Session, "request")

    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = json.dumps(embedding_response, ensure_ascii=False).encode(
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

    result = openai.Embedding.create(
        input="sample text",
        model="text-similarity-davinci-001",
    )

    assert not hasattr(result, "pipeline_run_id")


def test_openai_completion_self_contained_pipeline_id_server(mocker):
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()

    openai.api_key = os.getenv("OPENAI_KEY")

    result = openai.Embedding.create(
        input="sample text",
        model="text-similarity-davinci-001",
        pipeline_id="testing-value",
    )

    assert uuid.UUID(result.pipeline_run_id)


def test_openai_completion_self_contained_no_pipeline_id_server(mocker):
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()

    openai.api_key = os.getenv("OPENAI_KEY")

    result = openai.Embedding.create(
        input="sample text",
        model="text-similarity-davinci-001",
    )

    assert not hasattr(result, "pipeline_run_id")
