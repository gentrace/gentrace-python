import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

SET_ID = "9685b34e-2cac-5bd2-8751-c9e34ff9fd98"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api/v1"
)

cases = gentrace.get_test_cases(set_id=SET_ID)

for case in cases:
    print(case)
