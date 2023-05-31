import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GENTRACE_API_KEY")

print("GENTRACE_API_KEY: ", api_key)

set_id = "12494e89-af19-4326-a12c-54e487337ecc"

evaluation = gentrace.Evaluation(api_key=api_key, host="http://localhost:3000/api/v1")

cases = evaluation.get_test_cases(set_id=set_id)

results = []

for case in cases:
    results.append(
        {
            "caseId": case["id"],
            "inputs": {
                "a": "1",
                "b": "2",
            },
            "output": "This are some outputs",
        }
    )

result = evaluation.submit_test_results(set_id, "python-script", results)

print(result["runId"])
