import os
from unittest.mock import create_autospec

import pytest

import gentrace
from gentrace.providers.init import GENTRACE_CONFIG_STATE


def test_gentrace_no_host_valid():
    gentrace.init(api_key=os.getenv("GENTRACE_API_KEY"))

    gentrace.configure_openai()

    gentrace.deinit()


def test_gentrace_direct_api_key():
    os.environ["GENTRACE_API_KEY"] = ""

    gentrace.init(api_key="testing")

    gentrace.configure_openai()

    gentrace.deinit()


def test_gentrace_env_api_key():
    # Assuming that the test suite loads in a defined GENTRACE_API_KEY env variable
    gentrace.init()

    gentrace.configure_openai()

    gentrace.deinit()


def test_gentrace_localhost_host_valid():
    with pytest.raises(ValueError):
        gentrace.init(
            api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000"
        )

    with pytest.raises(ValueError):
        gentrace.init(
            api_key=os.getenv("GENTRACE_API_KEY"),
            host="http://localhost:3000/api/v1/feedback",
        )

    gentrace.deinit()


def test_gentrace_staging_host_valid():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="https://staging.gentrace.ai/api/v1/",
    )

    gentrace.configure_openai()

    with pytest.raises(ValueError):
        gentrace.init(
            api_key=os.getenv("GENTRACE_API_KEY"),
            host="https://staging.gentrace.ai/api/v1/feedback",
        )

    gentrace.deinit()


def test_gentrace_prod_host_valid():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="https://gentrace.ai/api/v1/",
    )

    with pytest.raises(ValueError):
        gentrace.init(
            api_key=os.getenv("GENTRACE_API_KEY"),
            host="https://gentrace.ai/api/v1/feedback",
        )

    gentrace.deinit()


def test_openai_configure_should_raise_error():
    with pytest.raises(ValueError):
        gentrace.configure_openai()


def test_openai_configure_should_not_raise_error():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
    )

    gentrace.configure_openai()

    gentrace.deinit()


def test_pinecone_configure_should_raise_error():
    with pytest.raises(ValueError):
        gentrace.configure_pinecone()


def test_pinecone_configure_should_not_raise_error():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
    )

    gentrace.configure_pinecone()

    gentrace.deinit()


def test_pipeline_should_not_raise_error():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host="http://localhost:3000/api/v1",
    )

    pipeline = gentrace.Pipeline(
        "test-gentrace-python-pipeline",
        openai_config={
            "api_key": os.getenv("OPENAI_KEY"),
        },
    )

    gentrace.deinit()


def test_pipeline_should_raise_error():
    with pytest.raises(ValueError):
        gentrace.Pipeline(
            "test-gentrace-python-pipeline",
            openai_config={
                "api_key": os.getenv("OPENAI_KEY"),
            },
        )

    gentrace.deinit()
