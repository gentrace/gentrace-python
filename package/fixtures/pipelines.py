import pytest


@pytest.fixture
def pipelines():
    return {
        "pipelines": [
            {
                "id": "9685b34e-2cac-5bd2-8751-c9e34ff9fd98",
                "createdAt": "2023-07-18T11:08:09.842Z",
                "updatedAt": "2023-07-18T11:08:09.842Z",
                "archivedAt": None,
                "labels": ["guessing"],
                "name": "Guess the Year",
                "organizationId": "fe05eab7-4f07-530d-8ed9-15aeae86e0db",
                "branch": "main",
                "cases": [
                    {
                        "id": "316c3797-7d04-54f9-91f0-8af87e1c8413",
                        "createdAt": "2023-07-18T11:08:09.863Z",
                        "updatedAt": "2023-07-18T11:08:09.863Z",
                        "archivedAt": None,
                        "expected": "2023",
                        "expectedSteps": None,
                        "inputs": {
                            "query": "In what year was the Apple Vision Pro released?"
                        },
                        "name": "Apple Vision Pro released",
                        "setId": "9685b34e-2cac-5bd2-8751-c9e34ff9fd98",
                    },
                    {
                        "id": "a2bddcbc-51ac-5831-be0d-5868a7ffa1db",
                        "createdAt": "2023-07-18T11:08:09.861Z",
                        "updatedAt": "2023-07-18T11:08:09.861Z",
                        "archivedAt": None,
                        "expected": "2022",
                        "expectedSteps": None,
                        "inputs": {"query": "In what year was ChatGPT released?"},
                        "name": "ChatGPT released",
                        "setId": "9685b34e-2cac-5bd2-8751-c9e34ff9fd98",
                    },
                    {
                        "id": "275d92ac-db8a-5964-846d-c8a7bc3caf4d",
                        "createdAt": "2023-07-18T11:08:09.858Z",
                        "updatedAt": "2023-07-18T11:08:09.858Z",
                        "archivedAt": None,
                        "expected": "2023",
                        "expectedSteps": None,
                        "inputs": {"query": "In what year was Gentrace founded?"},
                        "name": "Gentrace founded",
                        "setId": "9685b34e-2cac-5bd2-8751-c9e34ff9fd98",
                    },
                ],
            },
            {
                "id": "393e926e-ba1b-486f-8cbe-db7d9471fe56",
                "createdAt": "2023-07-18T12:47:58.618Z",
                "updatedAt": "2023-07-18T12:47:58.618Z",
                "archivedAt": None,
                "labels": [],
                "name": "Testign",
                "organizationId": "fe05eab7-4f07-530d-8ed9-15aeae86e0db",
                "branch": "main",
                "cases": [],
            },
        ]
    }
