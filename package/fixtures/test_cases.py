import pytest


@pytest.fixture
def test_cases():
    return {
        "testCases": [
            {
                "id": "b19fd229-c74b-56ee-a421-96d3670cfbdb",
                "createdAt": "2023-06-02T16:56:07.082Z",
                "updatedAt": "2023-06-02T16:56:07.082Z",
                "archivedAt": None,
                "expected": "Niagara Falls",
                "inputs": {
                    "question": "What is the name of the famous waterfall located on the border of Canada and the United States?"
                },
                "name": "Test Case 25",
                "pipelineId": "09c6528e-5a2b-548b-b666-c0cb71e12145",
            },
            {
                "id": "af8a20f1-73f3-5e57-8ab8-577d70a5bc96",
                "createdAt": "2023-06-02T16:56:07.082Z",
                "updatedAt": "2023-06-02T16:56:07.082Z",
                "archivedAt": None,
                "expected": "Disneyland",
                "inputs": {
                    "question": "What is the name of the famous theme park located in Anaheim, United States?"
                },
                "name": "Test Case 44",
                "pipelineId": "09c6528e-5a2b-548b-b666-c0cb71e12145",
            },
            {
                "id": "032e1643-9caa-5fbc-96a8-b55e971d726e",
                "createdAt": "2023-06-02T16:56:07.082Z",
                "updatedAt": "2023-06-02T16:56:07.082Z",
                "archivedAt": None,
                "expected": "Mount Fuji",
                "inputs": {
                    "question": "What is the name of the famous mountain located in Japan that is also an active volcano?"
                },
                "name": "Test Case 30",
                "pipelineId": "09c6528e-5a2b-548b-b666-c0cb71e12145",
            },
        ]
    }
