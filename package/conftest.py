import os

import pytest
from dotenv import load_dotenv

import gentrace
from fixtures.aioresponse import mockaio
from fixtures.chat_completion import chat_completion_response
from fixtures.completion import completion_response
from fixtures.embedding import embedding_response
from fixtures.gentrace import gentrace_pipeline_run_response
from fixtures.multiple_create_tc import multiple_create_tc
from fixtures.pipelines import pipelines
from fixtures.single_create_tc import single_create_tc
from fixtures.submit_test_run import test_run_response
from fixtures.test_cases import test_cases
from fixtures.test_result_response import test_result_response
from fixtures.update_tc import update_tc
from fixtures.vector import vector


@pytest.fixture()
def setup_teardown_openai():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
    )

    gentrace.configure_openai()

    yield "done"

    gentrace.deinit()


@pytest.fixture()
def setup_teardown_pinecone():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
    )

    gentrace.configure_pinecone()

    yield "done"
    gentrace.deinit()


def setup():
    print("Invoking setup")


def pytest_configure():
    load_dotenv()
