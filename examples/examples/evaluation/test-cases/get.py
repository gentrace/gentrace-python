import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

CASE_ID = "316c3797-7d04-54f9-91f0-8af87e1c8413"

case = gentrace.get_test_case(case_id=CASE_ID)

print("case", case.get('createdAt'))
