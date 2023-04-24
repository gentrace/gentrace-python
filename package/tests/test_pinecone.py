import http.client
import io
import json
import os
import random
import re
import uuid

import openai
import pytest
import requests
import responses
from urllib3.response import HTTPResponse

import gentrace

PINECONE_API_PATTERN = re.compile("^https?:\/\/.*pinecone\.io\/.*")


def test_pinecone_fetch_server():
    responses.add_passthru(PINECONE_API_PATTERN)

    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
        pinecone_config={
            "api_key": os.getenv("PINECONE_API_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    pinecone = runner.get_pinecone()

    index = pinecone.Index("openai-trec")

    index.fetch(ids=["3980"])

    info = runner.submit()

    assert uuid.UUID(info["pipelineRunId"]) is not None


def test_pinecone_query_server(vector):
    responses.add_passthru(PINECONE_API_PATTERN)

    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
        pinecone_config={
            "api_key": os.getenv("PINECONE_API_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    pinecone = runner.get_pinecone()

    index = pinecone.Index("openai-trec")

    index.query(top_k=10, vector=vector, pipline_id="self-contained-pinecone-query")

    info = runner.submit()

    assert uuid.UUID(info["pipelineRunId"]) is not None


def test_pinecone_list_indices():
    responses.add_passthru(PINECONE_API_PATTERN)

    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
        pinecone_config={
            "api_key": os.getenv("PINECONE_API_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    pinecone = runner.get_pinecone()

    active_indexes = pinecone.list_indexes()

    # liste_indexes is not supported, do not send information
    info = runner.submit()

    assert info["pipelineRunId"] is None


def test_pinecone_upsert(vector):
    responses.add_passthru(PINECONE_API_PATTERN)

    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
        pinecone_config={
            "api_key": os.getenv("PINECONE_API_KEY"),
        },
    )

    pipeline.setup()

    runner = pipeline.start()

    pinecone = runner.get_pinecone()

    pinecone.Index("openai-trec").upsert(
        [
            {
                "id": str(random.randint(0, 9999)),
                "values": vector,
            },
        ],
        pipeline_id="self-contained-pinecone-upsert",
    )

    # list_indexes is not supported, do not send information
    info = runner.submit()

    assert uuid.UUID(info["pipelineRunId"]) is not None
