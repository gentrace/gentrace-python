import os

import pytest
from dotenv import load_dotenv

import gentrace


@pytest.fixture()
def setup_teardown_openai():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host=os.getenv("GENTRACE_HOSTNAME") if os.getenv("GENTRACE_HOSTNAME") else "https://gentrace.ai/api",
    )

    yield "done"

    gentrace.deinit()


@pytest.fixture()
def setup_teardown_pinecone():
    gentrace.init(
        api_key=os.getenv("GENTRACE_API_KEY"),
        host=os.getenv("GENTRACE_HOSTNAME") if os.getenv("GENTRACE_HOSTNAME") else "https://gentrace.ai/api",
    )

    gentrace.configure_pinecone()

    yield "done"
    gentrace.deinit()


def setup():
    print("Invoking setup")


def pytest_configure():
    load_dotenv()
