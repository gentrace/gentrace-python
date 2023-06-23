import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

SET_ID = "e605d843-88e0-4462-85cc-2d49b0217a30"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
)

cases = gentrace.get_test_cases(set_id=SET_ID)

for case in cases:
    print(case)
