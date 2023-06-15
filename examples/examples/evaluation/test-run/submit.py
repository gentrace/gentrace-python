import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

SET_ID = "42d88419-4930-471c-beb9-297fabb8f970"


gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
)

cases = gentrace.get_test_cases(set_id=SET_ID)

results = []

for case in cases:
    results.append(
        "This are some outputs"
    )

result = gentrace.submit_test_results(SET_ID, test_cases=cases, outputs=results)

print(result["runId"])
