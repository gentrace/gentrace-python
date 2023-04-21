import os
from unittest.mock import create_autospec

import openai

import gentrace


def test_openai_completion(mocker):
    gentrace.host = "http://localhost:3000/api/v1"

    gentrace.configure_openai()

    openai.api_key = os.getenv("OPENAI_KEY")

    result = openai.Embedding.create(
        input="sample text",
        model="text-similarity-davinci-001",
        pipeline_id="testing-value",
    )

    assert result.pipeline_run_id
