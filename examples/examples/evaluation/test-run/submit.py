import os
from typing import List

import gentrace
from dotenv import load_dotenv
from gentrace.providers.evaluation import OutputStep

load_dotenv()

SET_ID = "9685b34e-2cac-5bd2-8751-c9e34ff9fd98"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    run_name="vivek python run",
    host="http://localhost:3000/api/v1",
)

cases = gentrace.get_test_cases(set_id=SET_ID)

outputs_list = []

for case in cases:
    outputs_list.append({ 
        "values": "This are some outputs", 
        "steps": [{"key": "compose", "output": "Testing information"}]
    })

result = gentrace.submit_test_result(
    SET_ID, test_cases=cases, outputs_list=outputs_list
)

print(result["runId"])
