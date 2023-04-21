import pytest


@pytest.fixture
def embedding_response():
    return {
        "data": [
            {
                "embedding": "",
                "index": 0,
                "object": "embedding",
            }
        ],
        "model": "text-similarity-davinci:001",
        "object": "list",
        "usage": {"prompt_tokens": 2, "total_tokens": 2},
    }
