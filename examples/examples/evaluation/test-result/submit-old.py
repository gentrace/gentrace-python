import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    run_name="vivek python run",
    host="http://localhost:3000/api",
)

cases = gentrace.get_test_cases(pipeline_slug="testing3")

outputs_list = []

for case in cases:
    outputs_list.append(
        {
            "values": "This are some outputs",
            "steps": [{"key": "compose", "output": "Testing information"}],
        }
    )

result = gentrace.submit_test_result(
    "testing3", test_cases=cases, outputs_list=outputs_list, context={
      "metadata": {
        "promptString": {
          "type": "string",
          "value": "testing"
        }
      }
    }
)

print(result["resultId"])
