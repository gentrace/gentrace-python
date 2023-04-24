import os
from unittest.mock import create_autospec

import pytest
from urllib3.response import HTTPResponse

import gentrace


def test_should_raise_error():
    with pytest.raises(ValueError):
        gentrace.configure_openai()

    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"


def test_should_not_raise_error():
    gentrace.api_key = os.getenv("GENTRACE_API_KEY")
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()
