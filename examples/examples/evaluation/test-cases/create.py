import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

case_id = gentrace.create_test_case(
    dataset_id="70a96925-db53-5c59-82b4-f42e988950a9",
    payload={
        "name": "Updated test case name",
        "inputs": {"d": 1},
        "expectedOutputs": {"e": 2},
    },
)

print(case_id)
