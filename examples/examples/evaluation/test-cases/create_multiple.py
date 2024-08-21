import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

response = gentrace.create_test_cases(
    pipeline_slug="main",
    dataset_id="70a96925-db53-5c59-82b4-f42e988950a9",
    payload=[
        {
            "name": "Batman -> Black Window #1",
            "inputs": {
                "query": "describing an ethical dilemma you encountered and asking "
                + "for feedback",
                "sender": "Batman",
                "receiver": "Black Widow",
            },
        },
        {
            "name": "Superman -> Wonder Woman #3",
            "inputs": {
                "query": "desperately asking for backup to a tough situation you am"
                + " in",
                "sender": "Superman",
                "receiver": "Wonder Woman",
            },
            "expectedOutputs": {
                "value": "Subject: Urgent Assistance Required: Backup Needed"
                + " Immediately"
            },
        },
    ],
)

print(response)
