import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api/v1"
)

result = gentrace.get_test_result("ede8271a-699f-4db7-a198-2c51a99e2dab")

print(result)
