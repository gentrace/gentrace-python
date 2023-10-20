import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

cases = gentrace.get_test_cases(pipeline_slug="testing-pipeline-id")

for case in cases:
    print(case)
