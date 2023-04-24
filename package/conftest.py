import os

import pytest
from dotenv import load_dotenv

import gentrace
from fixtures.aioresponse import mockaio
from fixtures.completion import completion_response
from fixtures.embedding import embedding_response
from fixtures.gentrace import gentrace_pipeline_run_response
from fixtures.vector import vector


@pytest.fixture()
def setup_teardown_openai():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()

    yield "done"
    gentrace.api_key = ""
    gentrace.host = ""


@pytest.fixture()
def setup_teardown_pinecone():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_pinecone()

    yield "done"
    gentrace.api_key = ""
    gentrace.host = ""


def setup():
    print("Invoking setup")


def pytest_configure():
    load_dotenv()
