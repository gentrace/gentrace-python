import json
from unittest.mock import create_autospec

import openai
import requests

import gentrace


def test_openai_completion(mocker, embedding_response):
    gentrace.configure_openai()

    # Setup OpenAI mocked request
    openai_api_key_getter = mocker.patch.object(openai.util, "default_api_key")
    openai_api_key_getter.return_value = "test-key"

    openai_request = mocker.patch.object(requests.sessions.Session, "request")

    response = requests.Response()
    response.status_code = 200
    response.headers["Content-Type"] = "application/json"
    response._content = json.dumps(embedding_response, ensure_ascii=False).encode(
        "utf-8"
    )
    
    openai_request.return_value = response
    
    # Setup Gentrace mocked response
    gentrace_request = mocker.patch.object(gentrace.PipelineRun, "submit")

    result = openai.Embedding.create(
        input="sample text",
        model="text-similarity-davinci-001",
        pipeline_id="testing-value",
    )

    print("Result: ", result.pipeline_run_id)
