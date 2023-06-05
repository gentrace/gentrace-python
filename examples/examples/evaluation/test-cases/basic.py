import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GENTRACE_API_KEY")

print("GENTRACE_API_KEY: ", api_key)

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
)

cases = gentrace.get_test_cases(set_id="09c6528e-5a2b-548b-b666-c0cb71e12145")

for case in cases:
    print("case: ", case, case["updatedAt"], case["name"], case["id"])
