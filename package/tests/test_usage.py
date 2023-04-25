import os
import re
from unittest.mock import create_autospec

import pytest
from urllib3.response import HTTPResponse

import gentrace


def test_gentrace_host_valid():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/"

    with pytest.raises(ValueError):
        gentrace.configure_openai()

    gentrace.host = "http://localhost:3000/api/v1/feedback"
    with pytest.raises(ValueError):
        gentrace.configure_openai()

    gentrace.host = ""
    gentrace.api_key = ""


def test_openai_configure_should_raise_error():
    with pytest.raises(ValueError):
        gentrace.configure_openai()


def test_openai_configure_should_not_raise_error():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()

    gentrace.api_key = ""
    gentrace.host = ""


def test_pinecone_configure_should_raise_error():
    with pytest.raises(ValueError):
        gentrace.configure_pinecone()


def test_pinecone_configure_should_not_raise_error():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_pinecone()

    gentrace.api_key = ""
    gentrace.host = ""
