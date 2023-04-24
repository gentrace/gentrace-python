import os
from unittest.mock import create_autospec

import pytest
from urllib3.response import HTTPResponse

import gentrace


def test_openai_configure_should_raise_error():
    with pytest.raises(ValueError):
        gentrace.configure_openai()


def test_openai_configure_should_not_raise_error():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()


def test_pinecone_configure_should_not_raise_error():
    gentrace.configure_pinecone()
