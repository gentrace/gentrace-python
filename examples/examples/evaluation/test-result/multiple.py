import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

results = gentrace.get_test_results(pipeline_slug="testing-pipeline-id")

for result in results:
    print(result.get("id"))
