import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

result = gentrace.get_test_result("492ef124-aca1-4640-8c9c-641c874acdb7")

runs = result["runs"]

print("runs", runs)

run_ids = [run.get("id") for run in runs]

payloads = [
    {
        "note": "test note",
        "evaluatorId": "e1117752-01fe-568c-9ee0-5e160352031d",
        "runId": run_id,
        "evalLabel": "A",
    }
    for run_id in run_ids
]

creation_count = gentrace.bulk_create_evaluations(
    payload=payloads
)

print(creation_count)
