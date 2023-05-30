import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GENTRACE_API_KEY")

print("GENTRACE_API_KEY: ", api_key)

evaluation = gentrace.Evaluation(api_key=api_key, host="http://localhost:3000/api/v1")

cases = evaluation.get_test_cases(set_id="12494e89-af19-4326-a12c-54e487337ecc")

print("cases: ", cases)
