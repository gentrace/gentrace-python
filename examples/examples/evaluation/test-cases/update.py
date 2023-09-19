import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api/v1"
)

cases = gentrace.get_test_cases(pipeline_slug="testing-pipeline-id")

case_id = cases[0]["id"]

case_id = gentrace.update_test_case(
    pipeline_slug="testing-pipeline-id",
    payload={
        "id": case_id,
        "name": "Updated test case name",
    },
)

print(case_id)
