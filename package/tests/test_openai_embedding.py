import json
import os
import uuid

import pytest
from urllib3._collections import HTTPHeaderDict
from urllib3.response import HTTPResponse

import gentrace


def test_openai_embedding_self_contained_pipeline_id_sync(
        mocker, embedding_response, gentrace_pipeline_run_response, setup_teardown_openai
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

    result = openai_simple.embeddings.create(
        input="sample text",
        model="text-similarity-davinci-001",
        pipeline_slug="testing-value",
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print(setup_teardown_openai)


def test_openai_embedding_self_contained_no_pipeline_id_sync(
        mocker, embedding_response, gentrace_pipeline_run_response, setup_teardown_openai
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

    result = openai_simple.embeddings.create(
        input="sample text",
        model="text-similarity-davinci-001",
    )

    assert not hasattr(result, "pipelineRunId")
    print(setup_teardown_openai)


def test_openai_embedding_self_contained_pipeline_id_server_sync(
        mocker,
        gentrace_pipeline_run_response,
        setup_teardown_openai
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
    result = openai_simple.embeddings.create(
        input="sample text",
        model="text-similarity-davinci-001",
        pipeline_slug="testing-value-vivek",
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print("pipeline_id: ", result.pipelineRunId)
    print(setup_teardown_openai)


def test_openai_embedding_self_contained_no_pipeline_id_server_sync(mocker, setup_teardown_openai,
                                                                    gentrace_pipeline_run_response):
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

    result = openai_simple.embeddings.create(
        input="sample text",
        model="text-similarity-davinci-001",
    )

    assert not hasattr(result, "pipelineRunId")
    print(setup_teardown_openai)


def test_openai_embedding_pipeline_server_sync(setup_teardown_openai):
    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        host="http://localhost:3000/api",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai_advanced = runner.get_openai()

    openai_advanced.embeddings.create(input="sample text", model="text-similarity-davinci-001")

    info = runner.submit()

    assert uuid.UUID(info["pipelineRunId"]) is not None
    print(setup_teardown_openai)


def test_openai_embedding_pipeline_sync(
        mocker, embedding_response, gentrace_pipeline_run_response, setup_teardown_openai, httpx_mock
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/embeddings",
        json=embedding_response
    )

    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        host="http://localhost:3000/api",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai_handle = runner.get_openai()

    result = openai_handle.embeddings.create(
        input="sample text", model="text-similarity-davinci-001"
    )

    assert len(runner.step_runs) == 1

    info = runner.submit()

    assert uuid.UUID(info["pipelineRunId"]) is not None
    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_embedding_self_contained_no_pipeline_id_server_async(
        setup_teardown_openai,
):
    openai_simple = gentrace.AsyncOpenAI()

    result = await openai_simple.embeddings.create(
        input="sample text",
        model="text-similarity-davinci-001",
    )

    assert not hasattr(result, "pipelineRunId")
    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_embedding_self_contained_pipeline_id_server_async(
        setup_teardown_openai,
):
    openai_simple = gentrace.AsyncOpenAI()

    result = await openai_simple.embeddings.create(
        input="sample text",
        model="text-similarity-davinci-001",
        pipeline_slug="testing-value",
    )

    assert uuid.UUID(result.pipelineRunId) is not None

    print(setup_teardown_openai)


@pytest.mark.asyncio
async def test_openai_embedding_pipeline_async(
        mocker,
        httpx_mock,
        embedding_response,
        gentrace_pipeline_run_response,
        setup_teardown_openai,
):
    httpx_mock.add_response(
        method="POST",
        url="https://api.openai.com/v1/embeddings",
        json=embedding_response
    )

    headers = HTTPHeaderDict({"Content-Type": "application/json"})

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

    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        host="http://localhost:3000/api",
        openai_config={
            "api_key": "test-api-key",
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai_handle = runner.get_openai(asynchronous=True)

    await openai_handle.embeddings.create(
        input="sample text", model="text-similarity-davinci-001"
    )

    assert len(runner.step_runs) == 1

    info = await runner.asubmit()

    assert uuid.UUID(info["pipelineRunId"]) is not None

    print(setup_teardown_openai)


def test_openai_embedding_pipeline_server_with_slug_param(setup_teardown_openai):
    pipeline = gentrace.Pipeline(
        slug="test-gentrace-python-pipeline",
        host="http://localhost:3000/api",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    openai = runner.get_openai()

    openai.embeddings.create(input="sample text", model="text-similarity-davinci-001")

    info = runner.submit()

    assert uuid.UUID(info["pipelineRunId"]) is not None
    print(setup_teardown_openai)
