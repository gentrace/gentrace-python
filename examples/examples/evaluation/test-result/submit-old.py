import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    run_name="vivek python run",
    host="http://localhost:3000/api/v1",
)

cases = gentrace.get_test_cases(pipeline_slug="main")

outputs_list = []

for case in cases:
    outputs_list.append(
        {
            "values": "This are some outputs",
            "steps": [{"key": "compose", "output": "Testing information"}],
        }
    )

result = gentrace.submit_test_result(
    "main", test_cases=cases, outputs_list=outputs_list
)

print(result["resultId"])
