import json
import uuid

import pytest
import responses
from urllib3._collections import HTTPHeaderDict
from urllib3.response import HTTPResponse

import gentrace


def test_openai_completion_self_contained_pipeline_id_sync(
        mocker,
        httpx_mock,
        completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/completions",
        json={
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "Hello there! How can I assist you today?",
                        "role": "assistant"
                    }
                }
            ],
            "created": 1682626081,
            "id": "chatcmpl-7A2CH4dc97AMoLbQe79QZhe4dh3y9",
            "model": "gpt-3.5-turbo-0301",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 10,
                "prompt_tokens": 10,
                "total_tokens": 20
            }
        }
    )

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.OpenAI()

    result = openai_simple.completions.create(
        pipeline_slug="text-generation",
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print(setup_teardown_openai)


def test_openai_completion_self_contained_no_pipeline_id_sync(
        mocker,
        httpx_mock,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/completions",
        json={
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "Hello there! How can I assist you today?",
                        "role": "assistant"
                    }
                }
            ],
            "created": 1682626081,
            "id": "chatcmpl-7A2CH4dc97AMoLbQe79QZhe4dh3y9",
            "model": "gpt-3.5-turbo-0301",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 10,
                "prompt_tokens": 10,
                "total_tokens": 20
            }
        }
    )

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.OpenAI()

    result = openai_simple.completions.create(
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
    )

    assert not hasattr(result, "pipelineRunId")
    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_completion_self_contained_no_pipeline_id_async(
        mocker,
        httpx_mock,
        completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/completions",
        json={
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "Hello there! How can I assist you today?",
                        "role": "assistant"
                    }
                }
            ],
            "created": 1682626081,
            "id": "chatcmpl-7A2CH4dc97AMoLbQe79QZhe4dh3y9",
            "model": "gpt-3.5-turbo-0301",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 10,
                "prompt_tokens": 10,
                "total_tokens": 20
            }
        }
    )

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.AsyncOpenAI()

    result = await openai_simple.completions.create(
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
    )

    assert not hasattr(result, "pipelineRunId")

    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_completion_self_contained_pipeline_id_async(
        mocker,
        httpx_mock,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/completions",
        json={
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "Hello there! How can I assist you today?",
                        "role": "assistant"
                    }
                }
            ],
            "created": 1682626081,
            "id": "chatcmpl-7A2CH4dc97AMoLbQe79QZhe4dh3y9",
            "model": "gpt-3.5-turbo-0301",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 10,
                "prompt_tokens": 10,
                "total_tokens": 20
            }
        }
    )

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.AsyncOpenAI()

    result = await openai_simple.completions.create(
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
        pipeline_slug="test_openai_completion_self_contained_no_pipeline_id_async",
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print(setup_teardown_openai)


@responses.activate
def test_openai_completion_self_contained_pipeline_id_stream_sync(
        mocker,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.OpenAI()

    result = openai_simple.completions.create(
        pipeline_slug="text-generation",
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
        stream=True,
    )

    pipeline_run_id = None
    for value in result:
        pipeline_run_id = value.pipelineRunId

    assert uuid.UUID(pipeline_run_id) is not None

    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_completion_self_contained_pipeline_id_stream_async(
        setup_teardown_openai,
):
    openai_simple = gentrace.AsyncOpenAI()
    result = await openai_simple.completions.create(
        pipeline_slug="text-generation",
        model="text-davinci-003",
        prompt_template="Hello world {{ name }}",
        prompt_inputs={"name": "test"},
        stream=True,
    )

    pipeline_run_id = None
    async for value in result:
        pipeline_run_id = value.pipelineRunId

    assert uuid.UUID(pipeline_run_id) is not None

    print(setup_teardown_openai)


def test_openai_completion_self_contained_pipeline_id_prompt(
        mocker,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.OpenAI()

    result = openai_simple.completions.create(
        pipeline_slug="text-generation",
        model="text-davinci-003",
        prompt="Hello World",
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print(setup_teardown_openai)


def test_openai_completion_self_contained_no_pipeline_id_prompt(
        mocker,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.OpenAI()

    result = openai_simple.completions.create(
        model="text-davinci-003",
        prompt="Hello World",
    )

    assert not hasattr(result, "pipelineRunId")

    print(setup_teardown_openai)


def test_openai_completion_self_contained_pipeline_id_stream_prompt(
        mocker,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.OpenAI()

    result = openai_simple.completions.create(
        pipeline_slug="text-generation",
        model="text-davinci-003",
        prompt="Hello world!",
        stream=True,
    )

    pipeline_run_id = None
    for value in result:
        pipeline_run_id = value.pipelineRunId

    assert uuid.UUID(pipeline_run_id) is not None

    print(setup_teardown_openai)


@responses.activate
def test_openai_completion_self_contained_no_pipeline_id_stream_prompt(
        mocker,
        httpx_mock,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/completions",
        json={
            "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "Hello there! How can I assist you today?",
                        "role": "assistant"
                    }
                }
            ],
            "created": 1682626081,
            "id": "chatcmpl-7A2CH4dc97AMoLbQe79QZhe4dh3y9",
            "model": "gpt-3.5-turbo-0301",
            "object": "chat.completion",
            "usage": {
                "completion_tokens": 10,
                "prompt_tokens": 10,
                "total_tokens": 20
            }
        }
    )

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode(
        "utf-8"
    )
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    openai_simple = gentrace.OpenAI()

    result = openai_simple.completions.create(
        model="text-davinci-003",
        prompt="Hello world!",
        stream=True,
    )

    pipeline_run_id = None
    for value in result:
        if "pipelineRunId" in value:
            pipeline_run_id = value.pipelineRunId

    assert pipeline_run_id is None

    print(setup_teardown_openai)
