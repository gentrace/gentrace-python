import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

result = gentrace.get_test_result("0649dde6-79b2-460a-91be-2ffea9c44de2")

print(result)
