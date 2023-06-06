import json
import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

SET_ID = "09c6528e-5a2b-548b-b666-c0cb71e12145"

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"),
    host="http://localhost:3000/api/v1",
)

cases = gentrace.get_test_cases(set_id=SET_ID)

for case in cases:
    print(json.dumps(case, indent=4))
