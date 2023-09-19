import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api/v1"
)

case_id = gentrace.create_test_cases(
    pipeline_slug="testing-pipeline-id",
    payload={
        "testCases": [
            {
                "name": "Updated test case name multi 1",
                "inputs": {"d": 1},
                "expectedOutputs": {"e": 2},
            },
            {
                "name": "Updated test case name multi 2",
                "inputs": {"d": 1},
                "expectedOutputs": {"e": 2},
            },
        ]
    },
)

print(case_id)
