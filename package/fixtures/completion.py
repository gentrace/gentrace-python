import pytest


@pytest.fixture
def completion_response():
    return {
        "choices": [
            {"finish_reason": "stop", "index": 0, "logprobs": None, "text": "\n"}
        ],
        "created": 1682109134,
        "id": "cmpl-77riQulvtyXo30e14QwSxzGATk2a5",
        "model": "text-davinci-003",
        "object": "text_completion",
        "usage": {"completion_tokens": 1, "prompt_tokens": 3, "total_tokens": 4},
    }
