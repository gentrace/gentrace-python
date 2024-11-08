import os

import gentrace
from dotenv import load_dotenv

load_dotenv()

gentrace.init(
    api_key=os.getenv("GENTRACE_API_KEY"), host="http://localhost:3000/api"
)

DATASET_ID = "3631b909-693c-41ba-ab9a-5538028d269d"

dataset_cases = gentrace.get_test_cases(dataset_id=DATASET_ID)

print("Test cases for dataset:", DATASET_ID)
for case in dataset_cases:
    print(case)

