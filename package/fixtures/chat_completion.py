import pytest


@pytest.fixture
def chat_completion_response():
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "Hello there! How can I assist you today?",
                    "role": "assistant",
                },
            }
        ],
        "created": 1682626081,
        "id": "chatcmpl-7A2CH4dc97AMoLbQe79QZhe4dh3y9",
        "model": "gpt-3.5-turbo-0301",
        "object": "chat.completion",
        "usage": {"completion_tokens": 10, "prompt_tokens": 10, "total_tokens": 20},
    }
