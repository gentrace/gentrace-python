import json
import os
import uuid

import openai
import pytest
from urllib3._collections import HTTPHeaderDict
from urllib3.response import HTTPResponse

import gentrace


def test_openai_chat_completion_self_contained_pipeline_id_only(
        mocker,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
        httpx_mock,
):
    # Setup Gentrace mocked response
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode("utf-8")

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

    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
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
    openai_simple = gentrace.OpenAI()

    result = openai_simple.chat.completions.create(
        pipeline_slug="testing-chat-completion-value",
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-3.5-turbo",
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print(setup_teardown_openai)


def test_openai_chat_completion_self_contained_no_pipeline_id_sync(
        mocker,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
        httpx_mock
):
    # Setup Gentrace mocked response
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode("utf-8")

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

    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
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
    openai_simple = gentrace.OpenAI()

    result = openai_simple.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-3.5-turbo",
    )

    assert not hasattr(result, "pipelineRunId")
    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_chat_completion_self_contained_no_pipeline_id_async(
        httpx_mock,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
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
    openai_simple = gentrace.AsyncOpenAI()
    result = await openai_simple.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-3.5-turbo",
    )

    assert not hasattr(result, "pipelineRunId")

    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_chat_completion_self_contained_pipeline_id_async(
        mocker,
        httpx_mock,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
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
    openai_simple = gentrace.AsyncOpenAI()

    result = await openai_simple.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-3.5-turbo",
        pipeline_slug="test_openai_completion_self_contained_no_pipeline_id_async",
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print(setup_teardown_openai)


def test_openai_chat_completion_self_contained_pipeline_id_stream_sync(
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    openai_simple = gentrace.OpenAI(api_key=os.getenv("OPENAI_KEY"))

    result = openai_simple.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-3.5-turbo",
        pipeline_slug="test_openai_completion_self_contained_no_pipeline_id_async",
        stream=True,
    )

    pipeline_run_id = None
    for value in result:
        pipeline_run_id = value.pipelineRunId

    assert uuid.UUID(pipeline_run_id) is not None

    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_chat_completion_self_contained_pipeline_id_stream_async(
        setup_teardown_openai,
):
    openai_simple = gentrace.AsyncOpenAI(api_key=os.getenv("OPENAI_KEY"))
    result = await openai_simple.chat.completions.create(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-3.5-turbo",
        pipeline_slug="test_openai_completion_self_contained_no_pipeline_id_async",
        stream=True,
    )

    pipeline_run_id = None
    async for value in result:
        pipeline_run_id = value.pipelineRunId

    assert uuid.UUID(pipeline_run_id) is not None

    print(setup_teardown_openai)


def test_openai_chat_completion_self_contained_pipeline_id_template(
        mocker,
        httpx_mock,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    # Setup Gentrace mocked response
    headers = HTTPHeaderDict({"Content-Type": "application/json"})

    body = json.dumps(gentrace_pipeline_run_response, ensure_ascii=False).encode("utf-8")

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

    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
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

    openai_simple = gentrace.OpenAI()

    result = openai_simple.chat.completions.create(
        messages=[
            {
                "role": "user",
                "contentTemplate": "Hello world, {{ name }}!",
                "contentInputs": {"name": "Vivek"},
            }
        ],
        model="gpt-3.5-turbo",
        pipeline_slug="test_openai_completion_self_contained_no_pipeline_id_async",
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print(setup_teardown_openai)


def test_openai_chat_completion_self_contained_render_correctly_easy():
    from gentrace.providers.llms.openai_v0 import create_rendered_chat_messages

    new_messages = create_rendered_chat_messages(
        [
            {
                "role": "user",
                "contentTemplate": "Hello world, {{ name }}!",
                "contentInputs": {"name": "Vivek"},
            }
        ]
    )

    assert new_messages == [
        {
            "role": "user",
            "content": "Hello world, Vivek!",
        }
    ]


def test_openai_chat_completion_self_contained_render_correctly_multiple_values():
    from gentrace.providers.llms.openai_v0 import create_rendered_chat_messages

    new_messages = create_rendered_chat_messages(
        [
            {
                "role": "user",
                "contentTemplate": "Hello world, {{ name }}! Are you based in {{ location }}?",
                "contentInputs": {"name": "Vivek", "location": "London"},
            },
            {
                "role": "user",
                "content": "Hello world, Vivek! Are you based in London?",
            },
        ]
    )

    assert new_messages == [
        {
            "role": "user",
            "content": "Hello world, Vivek! Are you based in London?",
        },
        {
            "role": "user",
            "content": "Hello world, Vivek! Are you based in London?",
        },
    ]


def test_openai_completion_self_contained_no_pipeline_id_template(
        mocker,
        httpx_mock,
        chat_completion_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/chat/completions",
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

    result = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "contentTemplate": "Hello world, {{ name }}!",
                "contentInputs": {"name": "Vivek"},
            }
        ],
        model="gpt-3.5-turbo",
    )

    assert not hasattr(result, "pipelineRunId")

    print(setup_teardown_openai)
