import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

SET_ID = "e605d843-88e0-4462-85cc-2d49b0217a30"

gentrace.init(api_key=os.getenv("GENTRACE_API_KEY"), run_name="vivek python run")

cases = gentrace.get_test_cases(set_id=SET_ID)

results = []

for case in cases:
    results.append("This are some outputs")

result = gentrace.submit_test_results(SET_ID, test_cases=cases, outputs=results)

print(result["runId"])
