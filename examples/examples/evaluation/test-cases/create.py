import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

case_id = gentrace.create_test_case(
    pipeline_slug="testing-pipeline-id",
    payload={
        "name": "Updated test case name",
        "inputs": {"d": 1},
        "expectedOutputs": {"e": 2},
    },
)

print(case_id)
